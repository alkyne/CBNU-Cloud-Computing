import boto3
import sys

class Menu:

    def __init__(self):
        self.client = boto3.client('ec2')
        self.ec2 = boto3.resource('ec2')
        self.options = {
            1 : self.listInstances,
            3 : self.startInstance,
            5 : self.stopInstance,
            7 : self.rebootInstance,
            8 : self.listImages,
            99: self.byebye,
        }
    
    def displayMenu(self):
        print('---------------------------------------------------')
        print(' 1. list instance\t\t2. available zones')
        print(' 3. start instance\t\t4. available regions')
        print(' 5. stop instance\t\t6. create instance')
        print(' 7. reboot instance\t\t8. list images')
        print('\t\t\t\t99. quit')
        print('---------------------------------------------------')

    def runner(self):
        # runner
        self.displayMenu()
        print("Input menu : ", end='')
        action = self.options.get(int(input()))
        if action:
            action()
        else:
            print("hey what ?!?") # invalid menu

    def inputInstanceId(self):
        print("Instance Id : ", end='')
        self.instanceId = input()

    def listInstances(self):
        allInstances = self.ec2.instances.all()
        
        print ("Listing instances....")
        for x in allInstances:
            instanceId = x.id
            instanceName = x.tags[0]['Value']
            instanceAmi = x.image_id
            state = x.state['Name']
            instanceType = x.instance_type
            privateAddr = x.private_ip_address

            print ("[ID] : %s [name] : %s [AMI] : %s [type] : %s [state] : %s [IP] : %s" %(instanceId, instanceName, instanceAmi, instanceType, state, privateAddr))
            # print(dir(x))
    
    def startInstance(self):
        self.inputInstanceId()
        instance = self.ec2.Instance(self.instanceId)
        instanceState = instance.state['Name'] # get instance state
        if instanceState == 'stopped':
            res = instance.start() # start instance
            res = str(res)
            if res.find("pending") != -1:
                print ("Instance [%s] successfully started." % self.instanceId)
        else:
            print ("Instance [%s] is already running." % self.instanceId)

    def stopInstance(self):
        self.inputInstanceId()
        instance = self.ec2.Instance(self.instanceId)
        instanceState = instance.state['Name'] # get instance state
        if instanceState == 'running':
            res = instance.stop() # stop instance
            res = str(res)
            if res.find("stopping") != -1:
                print ("Instance [%s] successfully stopped." % self.instanceId)
        else:
            print ("Instance [%s] is not running." % self.instanceId)
    
    def rebootInstance(self):
        self.inputInstanceId()
        instance = self.ec2.Instance(self.instanceId)
        instanceState = instance.state['Name'] # get instance state
        if instanceState == 'running':
            instance.reboot() # reboot instance
            print ("rebooting [%s]..." % instanceId)

    def listImages(self):
        allImages = self.client.describe_images(Owners=['self'])
        
        print("[ImageID] %s [Name] %s [Owner] %s" )

    def byebye(self):
        print("bye bye")
        sys.exit(0)

if __name__ == '__main__':
    while True:
        m = Menu().runner()
        del m