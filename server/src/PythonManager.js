const exec = require('child_process').exec

module.exports = class PythonManager {
    constructor() {
        this.process = null
        this.pythonScript = '../driver/app.py'
    }

    startProcess() {
        console.log("> Starting python process")
        this.process = exec('python3 ' + this.pythonScript)
        this.process.stdout.on('data', (data) => {
            console.log("D:", data)
        })
        this.process.stderr.on('data', (data) => {
            console.log("ERR:", data)
        })
        this.process.on('close', () => {
            console.log("Python process closed, restarting in 2 secs")
            setTimeout(() => {
                this.startProcess()
                return;
            }, 2000)
        })
    }
}