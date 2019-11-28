# We Robot Eurobot 2020 Autonomus Robot

The architecture is divided in 3 distincs parts:

- the `driver` code, created in Python, this is the code that drive the robot, main logic of the navigation
- the `dash` code, created in React, this is the front-end, user interface of this whole system. This interface can be handy to configure the robot, simulate the robot and assist the creation of the robot driver code by providing a pretty graphic simulation of the table.
- the `server` code, written in Node.js, which supervise the driver process, recover it in case of a crash and connect the dashboard to the driver throught a websocket connexion. 

