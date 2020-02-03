import React from 'react';
import Two from 'two.js';
import Button from '@material-ui/core/Button';
import { Card, Grid } from '@material-ui/core';
import Io from 'socket.io-client'

//import Eel from './eel'

import 'xterm/css/xterm.css'
import Nipple from 'nipplejs'

import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'

export default class App extends React.Component {

  constructor() {
    super()
    this.state = {
      robot: {x: '0.00', y: '0.00', theta: 0},
      mouse: {
        position: {x: '0.00', y: '0.00'},
        vector: {
          length: '0.00',
          x: '0.00',
          y: '0.00'
        }
      },
      paused: false,
      mesure: false,
      mesuredLength: '0.00',
      gotoMode: false
    }
    this.canvas = null
    this.two = null
    this.canvasWidth = 0;
    this.canvasHeight = 0;

    //this.onWindowResize = this.onWindowResize.bind(this);
    this.onCanvasMouseMouve = this.onCanvasMouseMouve.bind(this);
    this.onCanvasClick = this.onCanvasClick.bind(this);
    this.toggleMesure = this.toggleMesure.bind(this)
    this.forward = this.forward.bind(this)
    this.resetPosition = this.resetPosition.bind(this)
    this.stop = this.stop.bind(this)
    this.crossGroup = null
    this.mesurePoints = []
    this.mouseCapture = false
    this.socket = null
    this.goto = this.goto.bind(this);
  }

  render() {
    return <div>
      <div id="terminal"></div>
      <div className="board-row">
        <div className="canvas-container-container">
          <div className="canvas-container">
              <div className="rect" id="canvas">
              
              </div>
          </div>
        </div>
        <div className="control-panel">
          <h2>Control Panel</h2>
          <Grid container className="coordinate-container" spacing={2}>
            <Grid item>
              <Card className="coordinate-card" xs={12} md={6}>
                <pre className="coordinate-x">X: {this.state.robot.x}</pre>
                <pre className="coordinate-y">Y: {this.state.robot.y}</pre>
                <pre className="coordinate-t">θ: {this.state.robot.theta}</pre>
              </Card>
            </Grid>
            <Grid item>
              <Card className="coordinate-card" xs={12} md={6}>
                {this.state.mesure &&
                  <div>
                    <pre className="coordinate-x">X: {this.state.mouse.vector.x}</pre>
                    <pre className="coordinate-y">Y: {this.state.mouse.vector.y}</pre>
                    <pre className="coordinate-t">Length: {this.state.mouse.vector.length}</pre>
                  </div>
                }
                {!this.state.mesure &&
                  <div>
                    <pre className="coordinate-x">Mouse X: {this.state.mouse.position.x}</pre>
                    <pre className="coordinate-y">Mouse Y: {this.state.mouse.position.y}</pre>
                  </div>}
              </Card>
            </Grid>
          </Grid>
          <Button variant="contained" color="primary" onClick={this.toggleMesure} style={{marginTop: '1em'}}>
            {this.state.mesure &&
              <span>Cancel</span>
            }
            {!this.state.mesure &&
              <span>Mesure</span>
            }
          </Button>
          <Button variant="contained" color="primary" onClick={this.goto} style={{marginTop: '1em'}}>
            Go TO
          </Button>
          <Button variant="contained" color="secondary" onClick={this.resetPosition} style={{marginTop: '1em'}}>
            Reset
          </Button>
          {/* <Button variant="contained" color="primary" onMouseDown={this.forward} onMouseUp={this.stop} style={{marginTop: '1em'}}>
            Forward
          </Button> */}
          <Button variant="contained" color="primary" onClick={this.stop} style={{marginTop: '1em'}}>
            Stop
          </Button>
          <div className="joystick-container" id="joystick-container">

          </div>
        </div>
      </div>
    </div>
  }
  
  toX = (coordinate) => (coordinate*this.canvasWidth)/3000

  toY = (coordinate) => (coordinate*this.canvasHeight)/2000

  fromX = (coordinate) => (coordinate*3000)/this.canvasWidth

  fromY = (coordinate) => (coordinate*2000)/this.canvasHeight

  forward() {
    console.log('Forward')
  }

  stop() {
    console.log('Stop')
    this.socket.send(JSON.stringify({
        cmd: 'stop'
    }))
  }

  resetPosition() {
    console.log('Reset position')
    this.socket.send(JSON.stringify({
        cmd: 'reset_pos'
    }))
  }

  goto() {
    console.log('toggle goto')
    this.socket.send(JSON.stringify({
        cmd: 'goto', 
        args: {
            x: parseFloat(this.state.mouse.position.x),
            y: parseFloat(this.state.mouse.position.y)
        }
    }))
  }

  onCanvasMouseMouve(event) {
    if (this.state.paused) {
      return;
    }
    let mouseX, mouseY = 0;

    let offsetX = this.canvas.offsetLeft;
    let offsetY = this.canvas.offsetTop;
    let element = this.canvas.offsetParent;

    while(element != null) {
        offsetX = parseInt(offsetX) + parseInt(element.offsetLeft);
        offsetY = parseInt(offsetY) + parseInt(element.offsetTop);
        element = element.offsetParent;
    }

    mouseX = this.fromX(event.pageX - offsetX)
    mouseY = this.fromY(event.pageY - offsetY)
    
    if (!this.mouseCapture) {
      this.setState({mouse: {vector: this.state.mouse.vector, position: {x: mouseX.toFixed(2), y: mouseY.toFixed(2)}}})
    }
  }

  onCanvasClick() {

    if (this.state.mesure && this.crossGroup !== null && this.crossGroup.children.length === 5 && this.state.mesuredLength !== 0) {
      if (this.crossGroup !== null)
        this.crossGroup.remove()
      this.crossGroup = null
      this.setState({mesuredLength: 0})
      this.mesurePoints = []
    }

    if (this.state.mesure) {
      if (this.crossGroup === null) {
        this.crossGroup = this.two.makeGroup()
      }
      if (this.crossGroup.children.length < 2) {
        this.createCross()
        this.mesurePoints.push({
          x: this.state.mouse.position.x,
          y: this.state.mouse.position.y
        })
      }
      if (this.crossGroup.children.length === 2 && this.state.mesuredLength === 0) {
        // actually mesure
        // compute the modal
        // Math.sqrt((y_1 - y_2)**2 + (x_ 1 - x_2)**2)

        this.setState({mouse: {position: this.state.mouse.position, vector: {
          x: Math.abs(this.mesurePoints[0].x - this.mesurePoints[1].x).toFixed(2),
          y: Math.abs(this.mesurePoints[0].y - this.mesurePoints[1].y).toFixed(2),
          length: Math.sqrt(
            (this.mesurePoints[0].x - this.mesurePoints[1].x) ** 2 +
            (this.mesurePoints[0].y - this.mesurePoints[1].y) ** 2
          ).toFixed(2)
        }}})

        let modalLine = new Two.Line(
          this.toX(this.mesurePoints[0].x),
          this.toY(this.mesurePoints[0].y),
          this.toX(this.mesurePoints[1].x),
          this.toY(this.mesurePoints[1].y)
        )

        let xLine = new Two.Line(
          this.toX(this.mesurePoints[0].x),
          this.toY(this.mesurePoints[0].y),
          this.toX(this.mesurePoints[1].x),
          this.toY(this.mesurePoints[0].y)
        )

        let yLine = new Two.Line(
          this.toX(this.mesurePoints[1].x),
          this.toY(this.mesurePoints[0].y),
          this.toX(this.mesurePoints[1].x),
          this.toY(this.mesurePoints[1].y)
        )
        modalLine.stroke = 'green'
        modalLine.linewidth = 2
        xLine.stroke = 'blue'
        yLine.stroke = 'red'
        this.crossGroup.add(modalLine)
        this.crossGroup.add(yLine)
        this.crossGroup.add(xLine)
      }
    } else {
      if (this.mouseCapture) {
        this.mouseCapture = false
        return;
      }
      if (this.crossGroup !== null)
        this.crossGroup.remove()
        this.crossGroup = null
      if (this.crossGroup === null)
        this.crossGroup = this.two.makeGroup()

      this.mouseCapture = true
      this.createCross()
    }
    this.two.update()
  }

  createCross() {
    let group = new Two.Group()
    // group.add(new Two.Line(
    //   this.toX(this.state.mouse.position.x),
    //   this.toY(this.state.mouse.position.y) - 20,
    //   this.toX(this.state.mouse.position.x),
    //   this.toY(this.state.mouse.position.y) + 20,
    // ))
    // group.add(new Two.Line(
    //   this.toX(this.state.mouse.position.x) - 20,
    //   this.toY(this.state.mouse.position.y),
    //   this.toX(this.state.mouse.position.x) + 20,
    //   this.toY(this.state.mouse.position.y),
    // ))
    let circle = new Two.Circle(
      this.toX(this.state.mouse.position.x), 
      this.toY(this.state.mouse.position.y), 3)

    circle.linewidth = 0
    circle.fill = 'blue'
    group.add(circle)
    this.crossGroup.add(group)
  }

  toggleMesure() {
    if (this.crossGroup !== null)
      this.crossGroup.remove()
    this.crossGroup = null
    this.mesurePoints = []
    this.setState({mesure: !this.state.mesure, mesuredLength: 0, mouse: {
      vector: {x: '0.00', y: '0.00', length: '0.00'},
      position: this.state.mouse.position
    }})
  }

  componentDidMount() { 
    // gritty('.terminal', {
    //     prefix: 'console',
    //     command: 'bash',
    //     autoRestart: true,
    //     cwd: '/',
    //     env: {
    //         TERMINAL: 'gritty'
    //     },
    //     socket: this.socket
    // });

    // const fitAddon = new FitAddon();
    // const terminal = new Terminal({
    //     scrollback: 1000,
    //     tabStopWidth: 4,
    //     fontFamily: 'Menlo, Consolas, "Liberation Mono", Monaco, "Lucida Console", monospace'
    // });
    
    // terminal.open(document.getElementById('terminal'));
    // terminal.focus();
    
    // terminal.loadAddon(fitAddon);
    // fitAddon.fit();
    
    // terminal.onResize(data => {
    //   console.log(data)
    //   //this.socket.emit('resize', data);
    // });
    // terminal.onData((data) => {
    //   this.socket.emit('data', data);
    // });

    // const {cols, rows} = terminal;

    // let autoRestart = true
    // let cwd = '/'
    // let command = 'bash'
    // let env = {}

    // this.socket.on('accept', () => {
    //   this.socket.emit('terminal', {env, cwd, cols, rows, command, autoRestart});
    //   this.socket.emit('resize', {cols, rows});
    //   fitAddon.fit();
    // });
    // this.socket.on('disconnect', () => {
    //   terminal.writeln('YAYAYAY terminal disconnected...');
    // });
    // this.socket.on('data', (dataPositionWatcher) => {
    //   terminal.write(data)
    // });
    
    // window.addEventListener('resize', () => {
    //   fitAddon.fit();
    // });
    // let joysticks = Nipple.create({
    //     zone: document.getElementById('joystick-container'),
    //     mode: 'static',
    //     position: {left: '50%', top: '50%'},
    //     color: 'blue'
    // });
    // let joystick = joysticks.get(0)
    
    // let joystickPosition = []
    // joystick.on('move', (evt, data) => {
    //     // let angle = data.angle.radian
    //     // let x = parseFloat(((Math.cos(angle) * data.distance)/50).toFixed(1))
    //     // let y = parseFloat(((Math.sin(angle) * data.distance)/50).toFixed(1))
    //     // //console.log([x, y])
        
    //     let x = 0.5
    //     let y = 1
    //     let a = data.angle.radian 
    //     if (a > 0 && a < Math.PI/6) {
    //         x = 1
    //         y = 0.1
    //     }
    //     if (a > Math.PI/2 && a < Math.PI) {
            
    //     }
    //     if (a > Math.PI && a < 3*Math.PI/2) {
            
    //     }
    //     if (a > 3*Math.PI/2 && a < 2*Math.PI) {
            
    //     }
    //     if (joystickPosition[0] !== x || joystickPosition[1] !== y) {
    //         this.socket.emit('motors', [x, y])
    //         joystickPosition = [x, y]
    //     }
    
    // });
    // joystick.on('end', () => {
    //     console.log('end')
    //     joystickPosition = [0, 0]
    //     this.socket.emit('stop')
    // });
    this.socket = new WebSocket("ws://192.168.0.19:8080");
    this.socket.onopen = () => {
      console.log('A direct connexion with the python driver programm was etablished')
    };
    this.socket.onmessage = (evt) => {
        let data = JSON.parse(evt.data)
        if (data.event === 'updatePosition') {
            let xCoordinate = data.data[0]
            let yCoordinate = data.data[1]
            let theta = data.data[2]
            console.log(xCoordinate, yCoordinate, theta)
            robotPoint.translation.x = robotGroup.translation.x = x(yCoordinate)
            robotPoint.translation.y = robotGroup.translation.y = y(xCoordinate)
            robotGroup.rotation = -theta + Math.PI/2
            this.two.update()
            this.setState({
                robot: {x: xCoordinate, y: yCoordinate, theta: (theta * 180/Math.PI).toFixed(2)}
            })
        }
    };

    this.canvas = document.getElementById('canvas')
    
    this.canvas.onmousemove = this.onCanvasMouseMouve
    this.canvas.onclick = this.onCanvasClick
    // get the real coordinate of x
    let x = (coordinate) => {
        return (coordinate*this.canvasWidth)/3000
    }

    // get the real coordinate of y
    let y = (coordinate) => {
        return (coordinate*this.canvasHeight)/2000
    }

    let canvasContainer = document.getElementsByClassName('canvas-container')[0]
    let robotGroup
    let robotPoint
    let render = () => {
        this.canvasWidth = canvasContainer.clientWidth
        this.canvasHeight = (2/3) * this.canvasWidth
        canvasContainer.setAttribute('style', 'height: ' + this.canvasHeight + 'px')
        this.canvas.innerHTML = ''
        this.two = new Two({
            width: '100%',
            height: this.canvasHeight,
            autostart: true
        }).appendTo(this.canvas)
      
        let anchor = [0, 0]
        let mainDiameter = x(276) - 1
        let mainRadius = mainDiameter/2
        robotGroup = this.two.makeGroup()
        let robotArc = new Two.ArcSegment(anchor[0], anchor[1], 0, mainRadius, 3*Math.PI/4, -3*Math.PI/4)
        let vert = robotArc.vertices.filter((v) => {
            return (v.x !== 0 && v.y !== 0)
        }).map((v) => {
            v.x = v.x + anchor[0]
            v.y = v.y + anchor[1]
            return v
        })
        let robotFill = new Two.Path(vert)
        robotFill.linewidth = 1
        robotGroup.add(robotFill)
        robotGroup.fill = '#c0392b'
        robotGroup.translation.x = x(98)
        robotGroup.translation.y = y(932)
        robotGroup.rotation = 0

        robotPoint = this.two.makeCircle(robotGroup.translation.x, robotGroup.translation.y, 2)
        this.two.update()
    }

    render()
    window.addEventListener('resize', render);
  }

  componentDidUpdate() {
    this.two.update();
  }
};
