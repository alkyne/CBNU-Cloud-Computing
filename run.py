import boto3
import sys

class Menu:

    def __init__(self):
        self.client = boto3.client('ec2')
        self.ec2 = boto3.resource('ec2')
        self.options = {
            1 : self.listInstances,
            2 : self.availableZones,
            3 : self.startInstance,
            5 : self.stopInstance,
            7 : self.rebootInstance,
            8 : self.listImages,
            9 : self.createImage,
            10: self.deleteImage,
            99: self.byebye,
        }

        self.runner() # run
    
    def displayMenu(self):
        print('---------------------------------------------------')
        print(' 1. list instance\t\t2. available zones')
        print(' 3. start instance\t\t4. available regions')
        print(' 5. stop instance\t\t6. create instance')
        print(' 7. reboot instance\t\t8. list images')
        print(' 9. (additional) create image')
        print(' 10. (additional) delete image')
        print('\t\t\t\t99. quit')
        print('---------------------------------------------------')

    def runner(self):
        # runner
        self.displayMenu() # print menu
        print("Input menu : ", end='')
        try:
            action = self.options.get(int(input()))
        except:
            print("nop")
            sys.exit(-1)

        if action:
            action()
        else:
            print("hey what ?!?") # invalid menu
        print()

    # get instanceId from user
    # and get that ec2 instance from AWS server
    def getInstance(self):
        print("Instance Id : ", end='')
        self.instanceId = input()
        try:
            self.instance = self.ec2.Instance(self.instanceId)
        except:
            print("Failed to load that instance.")

        return self.instance

    def availableZones(self):
        try:
            # load zones for state : available
            allZones = self.client.describe_availability_zones(Filters=[{'Name' : 'state', 'Values':['available']}])['AvailabilityZones']
        except :
            print("Failed to load available zones.", e)
            sys.exit(-1)

        print("Here are available zones : ")
        for x in allZones:
            zoneName = x['ZoneName']
            regionName = x['RegionName']
            print ("RegionName : %s, ZoneName : %s" % (regionName, zoneName))


    def listInstances(self):
        try:
            allInstances = self.ec2.instances.all()
        except:
            print("Failed to load instance list.")
            sys.exit(-1)
        
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
        instance = self.getInstance()
        instanceState = instance.state['Name'] # get instance state
        if instanceState == 'stopped':
            res = instance.start() # start instance
            res = str(res)
            if res.find("pending") != -1:
                print ("Instance [%s] successfully started." % self.instanceId)
        else:
            print ("Instance [%s] is already running." % self.instanceId)

    def stopInstance(self):
        instance = self.getInstance()
        instanceState = instance.state['Name'] # get instance state
        if instanceState == 'running':
            res = instance.stop() # stop instance
            res = str(res)
            if res.find("stopping") != -1:
                print ("Instance [%s] successfully stopped." % self.instanceId)
        else:
            print ("Instance [%s] is not running." % self.instanceId)
    
    def rebootInstance(self):
        instance = self.getInstance()
        instanceState = instance.state['Name'] # get instance state
        if instanceState == 'running':
            instance.reboot() # reboot instance
            print ("rebooting [%s]..." % self.instanceId)
        else:
            print("That instance is not running.")

    def listImages(self):
        try:
            imageDict = self.client.describe_images(Owners=['self'])
            allImages = imageDict['Images']
        except:
            print("Failed to load image list.")
            sys.exit(-1)

        print("Listing images....")
        for x in allImages:
            imageId = x['ImageId']
            imageName = x['ImageLocation'].split('/')[1]
            ownerId = x['OwnerId']    
            print("[ImageID] %s [Owner] %s [Name] %s" % (imageId, ownerId, imageName))

    def createImage(self):
        self.getInstance()
        print("New Image name : ", end='')
        imageName = input()

        try:
            self.client.create_image(InstanceId=self.instanceId, Name=imageName)
            print("Creating new image [%s] from [%s] done" % (imageName, self.instanceId))
        except:
            print("Failed to create new image.")
            sys.exit(-1)

    def deleteImage(self):
        print("Image id for deleting: ", end='')
        imageId = input()

        try:
            self.client.deregister_image(ImageId=imageId)
            print("Deleting image [%s] done" % (imageId))
        except:
            print("Failed to delete that image.")
            sys.exit(-1)

    def byebye(self):
        print("bye bye")
        sys.exit(0)

if __name__ == '__main__':
    while True:
        m = Menu()
        del m