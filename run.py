import boto3
import sys

#ec2 = boto3.client('ec2')

class Menu:

    def __init__(self):
        print('---------------------------------------------------')
        print(' 1. list instance\t\t2. available zones')
        print(' 3. start instance\t\t4. available regions')
        print(' 5. stop instance\t\t6. create instance')
        print(' 7. reboot instance\t\t8. list images')
        print('\t\t\t\t99. quit')
        print('---------------------------------------------------')

        self.option = 1
    
    def getOption(self):
        return self.option

class Runner:

    def __init__(self, option):
        # self.client = boto3.client('ec2')
        self.ec2 = boto3.resource('ec2')
        # self.option = option

    def listInstance(self):

        self.all_instances = self.ec2.instances.all()
        
        for x in self.all_instances:
            instanceId = x.id
            instanceName = x.tags[0]['Value']
            instanceAmi = x.image_id
            state = x.state['Name']
            instanceType = x.instance_type
            privateAddr = x.private_ip_address

            print ("[ID] : %s [name] : %s [AMI] : %s [type] : %s [state] : %s [IP] : %s" %(instanceId, instanceName, instanceAmi, instanceType, state, privateAddr))
            # print(dir(x))
    
    def startInstance(self):
        print("Instance Id : ")
        instanceId = input()
        instance = self.ec2.Instance(instanceId)
        instanceState = instance.state['Name']
        if instanceState == 'stopped':
            res = instance.start() # start instance
            res = str(res)
            if res.find("pending") != -1:
                print ("Instance [%s] successfully started." % instanceId)
        else:
            print ("Instance [%s] is already running." % instanceId)

    def stopInstance(self):
        print("Instance Id : ")
        instanceId = input()
        instance = self.ec2.Instance(instanceId)
        instanceState = instance.state['Name']
        if instanceState == 'running':
            res = instance.stop() # stop instance
            res = str(res)
            if res.find("stopping") != -1:
                print ("Instance [%s] successfully stopped." % instanceId)
        else:
            print ("Instance [%s] is not running." % instanceId)
    
    def rebootInstance(self):
        print("Instance Id : ")
        instanceId = input()
        instance = self.ec2.Instance(instanceId)
        instanceState = instance.state['Name']
        # if instanceState = 'running':

if __name__ == '__main__':
    # m = Menu()
    # r = Runner(m.getOption())
    # del m
    # del r
    # Runner(2).listInstance()
    Runner(2).stopInstance()

