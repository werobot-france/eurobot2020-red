print('> GOTO: ', {"x":targetX, "y":targetY, "threehold": threehold, "mustStop": mustStop, "backward": backward})
self.fetch()
a = 0
p, i, d = 190, 4, 550
#p, i, d = 190, 2, 400
vitesseC, vitesseR = 0.7 , 0.4
self.running = True
self.sommeErreurs = 0
distanceCibleI = sqrt((targetX-self.xR)*(targetX-self.xR)+(targetY-self.yR)*(targetY-self.yR))

while self.running:
    self.fetch()
    distanceCible = sqrt((targetX-self.xR)*(targetX-self.xR)+(targetY-self.yR)*(targetY-self.yR))
    targetTheta = atan2((targetY - self.yR), (targetX - self.xR))
    if (not backward):
        erreurOrientation = (targetTheta - self.orientation)
    else:
        erreurOrientation = (targetTheta - (self.orientation-pi))

    if mustStop: cmdG = cmdD = distanceCible
    else: cmdG = cmdD = distanceCibleI

    if cmdD > 255: cmdG = cmdD = 255
    
    cmdD *= vitesseC
    cmdG *= vitesseC

    if a == 0: self.erreurPre = (targetTheta - self.orientation)

    while abs(erreurOrientation) > pi:
        erreurOrientation += (-2*pi) * (erreurOrientation/abs(erreurOrientation))
        
    cmd = (erreurOrientation*p) + (self.sommeErreurs*i) + (self.differenceErreurs*d)
    cmdD += cmd
    cmdG -= cmd
    
    if cmdD > 255: cmdD = 255
    if cmdG > 255: cmdG = 255
    if cmdD < -255: cmdD = -255
    if cmdG < -255: cmdG = -255
    if abs(cmdG)<vitesseR*255 and cmdG != 0:cmdG = 255*vitesseR * cmdG/abs(cmdG)
    if abs(cmdD)<vitesseR*255 and cmdD != 0:cmdD = 255*vitesseR * cmdD/abs(cmdD)
    cmdD /= 255
    cmdG /= 255

    if a == 0:
        a+=1
        print('     Target:', (targetX, targetY))
        print('     Robot pos:', (self.xR, self.yR, self.orientation))
        print('     TargetTheta:', targetTheta)
        print('     Current error:', erreurOrientation)
        print('     Previous error:',self.erreurPre)
        print('     Distance to target:',distanceCible)
        print('     ', (('CMD', cmd), ('G', cmdG), ('D', cmdD)))
        print('     PID Factors:', (p, i, d))

    self.differenceErreurs = erreurOrientation - self.erreurPre
    self.sommeErreurs += erreurOrientation
    self.erreurPre = erreurOrientation
    
    try:
        if (not backward):
            self.leftMotor.throttle = cmdG
            self.rightMotor.throttle = cmdD
        else:
            self.leftMotor.throttle = -cmdD
            self.rightMotor.throttle = -cmdG
    except ValueError:
        print('_____________________ERREUR________________________')
        print(-cmdG, cmdD)
    if distanceCible < threehold:
        self.running = False
    print('     Position:', (self.xR, self.yR, degrees(self.orientation)))

print('Arrived! position:', (self.xR, self.yR, degrees(self.orientation)))
print('> GOTO exit')
if mustStop:
    self.stopMotors()
    self.goToOrientation(pi/2)