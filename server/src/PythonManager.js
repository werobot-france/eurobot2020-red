const spawn = require('child_process').spawn

module.exports = class PythonManager {
    constructor() {
        this.process = null
        this.pythonScript = '../driver/app.py'
    }

    startProcess() {
        console.log("> Starting python process")
        this.process = spawn('python3', [this.pythonScript])
        this.process.stdout.on('data', (data) => {
            console.log(data.toString())
            data = data.toString().replace("\n", '')
            if (data === "Initialization") {
                console.log('Python script Initialized, start position trace')
                this.write('start_position_trace')
                // {"cmd":"start_position_trace", "args": null}
            }
        })
        this.process.stderr.on('data', (data) => {
            console.log("ERR:", data.toString())
        })
        this.process.on('close', () => {
            console.log("Python process closed, restarting in 2 secs")
            setTimeout(() => {
                this.startProcess()
                return;
            }, 2000)
        })
    }

    write(cmd, args = null) {
        let toSend = JSON.stringify({cmd: cmd, args: args})
        console.log(toSend)
        this.process.stdin.write(toSend + "\n");
    }
}

