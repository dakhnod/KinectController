import body
import time
import numpy

class MovementReader:
    def __init__(self):
        self.isDodging = False
        self.isHandUp = False
        self.isRunningLeft = False
        self.isRunning = False
        self.lastFootUpWasLeft = False
        self.lastFootSwitchTime = 0
        self.hipHeightHistory = []
        self.isJumping = False
        self.isUsingItem = False

    def parse_movement(self, body):
        self._parse_running(body)
        self._parse_jump(body)
        self._parse_hook(body)
        self._parse_dodge(body)
        self._parse_item(body)

    def _parse_dodge(self, body):
        leftHandBelowHip = body.get_joint_HandLeft().y < body.get_joint_HipLeft().y
        rightHandBelowHip = body.get_joint_HandRight().y < body.get_joint_HipRight().y

        self.isDodging = leftHandBelowHip and rightHandBelowHip

    def _parse_hook(self, body):
        leftHandUp = body.get_joint_HandLeft().y > body.get_joint_ShoulderLeft().y
        rightHandUp = body.get_joint_HandRight().y > body.get_joint_ShoulderRight().y

        self.isHandUp = leftHandUp or rightHandUp

    def _parse_jump(self, body):
        hipHeight = (body.get_joint_HipLeft().y + body.get_joint_HipRight().y) / 2
        self.hipHeightHistory.append(hipHeight)

        averageWindowSize = 20
        if(len(self.hipHeightHistory) < averageWindowSize):
            return

        averageHipHeight = numpy.average(self.hipHeightHistory)
        hipHeightDeltaThreshold = 0.08
        hipHeightDelta = hipHeight - averageHipHeight
        self.isJumping = hipHeightDelta > hipHeightDeltaThreshold
        self.hipHeightHistory = self.hipHeightHistory[-averageWindowSize:]

    def _parse_running(self, body):
        footHeightDelta = body.get_joint_FootLeft().y - body.get_joint_FootRight().y

        footHeightThreshold = 0

        upperFootIsLeft = None
        anyFootIsUp = abs(footHeightDelta) >= footHeightThreshold
        if anyFootIsUp:
            upperFootIsLeft = footHeightDelta > 0

        self.isRunningLeft = (body.get_joint_HipLeft().z - body.get_joint_HipRight().z) > 0

        if anyFootIsUp and (upperFootIsLeft is not self.lastFootUpWasLeft):
            self.lastFootUpWasLeft = upperFootIsLeft
            self.lastFootSwitchTime = time.time()
            self.isRunning = True
        else:
            footSwitchLimit = 1
            lastFootSwitchDelta = time.time() - self.lastFootSwitchTime
            self.isRunning = lastFootSwitchDelta < footSwitchLimit

    def _parse_item(
        self, 
        body # type: body.Body
    ):
        leftHandBehindBack = body.get_joint_HandLeft().z > body.get_joint_HipLeft().z
        rightHandBehindBack = body.get_joint_HandRight().z > body.get_joint_HipRight().z

        self.isUsingItem = leftHandBehindBack or rightHandBehindBack