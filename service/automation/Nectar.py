import boto
from boto.ec2.regioninfo import RegionInfo
import time

from constant import DEPLOY_CONFIG_PATH
from similarity.Config import Config
from utils import logger


class Nectar:
    def __init__(self):
        access_key_id = Config(DEPLOY_CONFIG_PATH).get('nectar/access_key_id')
        access_key_secret = Config(DEPLOY_CONFIG_PATH).get('nectar/access_key_secret')
        region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
        self.ec2_conn = boto.connect_ec2(aws_access_key_id=access_key_id,
                                         aws_secret_access_key=access_key_secret,
                                         is_secure=True,
                                         region=region,
                                         port=8773,
                                         path='/Services/Cloud',
                                         validate_certs=False)

    def add_instance(self):
        instance_type = Config(DEPLOY_CONFIG_PATH).get('nectar/instance_type')
        keypair_name = Config(DEPLOY_CONFIG_PATH).get('nectar/keypair_name')
        security_groups = Config(DEPLOY_CONFIG_PATH).get('nectar/security_groups')
        zone = Config(DEPLOY_CONFIG_PATH).get('nectar/zone')
        image_id = self._get_image_id(Config(DEPLOY_CONFIG_PATH).get('nectar/image_name'))
        reservation = self.ec2_conn.run_instances(image_id=image_id,
                                                  key_name=keypair_name,
                                                  instance_type=instance_type,
                                                  security_groups=security_groups,
                                                  placement=zone)
        instance = reservation.instances[0]
        instance_info = {"id": instance.id, "ip": instance.private_ip_address, "state": instance.state}
        logger.info('Successfully created instance: {}'.format(instance_info))
        return instance_info

    def _get_image_id(self, image_name):
        images = self.list_image()
        filtered = list(filter(lambda x: x['name'] == image_name, images))
        if len(filtered) == 0:
            return None
        return [x['id'] for x in filtered][0]

    def list_instances(self):
        reservations = self.ec2_conn.get_all_instances()
        res = []

        for reservation in reservations:
            res.append({"id": reservation.instances[0].id,
                        "ip": reservation.instances[0].private_ip_address,
                        "state": reservation.instances[0].state})
        return res

    def list_image(self):
        images = self.ec2_conn.get_all_images()
        res = []
        for img in images:
            res.append({"id": img.id, "name": img.name})
        return res

    def list_volumes(self):
        volumes = self.ec2_conn.get_all_volumes()
        res = []
        for volume in volumes:
            res.append({"id": volume.id, "status": volume.status})
        return res

    def list_security_group(self):
        s_grp = self.ec2_conn.get_all_security_groups()
        res = []
        for grp in s_grp:
            res.append({"id": grp.id, "name": grp.name})
        return res

    def add_volume(self, instance_id):
        zone = Config(DEPLOY_CONFIG_PATH).get('nectar/zone')
        volume = self.ec2_conn.create_volume(size=50, zone=zone)
        info = self.get_volume_info(volume.id)
        while info["status"] != "available":
            logger.info("Volume state: " + info["status"])
            time.sleep(3)
            info = self.get_volume_info(volume.id)
        successful = volume.attach(instance_id, "/dev/vdc")
        if successful:
            logger.info("volume: " + volume.id + " set and bounded to /dev/vdc")
        else:
            logger.error("ERROR: volume creating failed.")

    def get_instance_info(self, instance_id):
        insts = self.list_instances()
        for inst in insts:
            if inst["id"] == instance_id:
                return inst
        return None

    def get_volume_info(self, volume_id):
        volumes = self.list_volumes()
        for volume in volumes:
            if volume["id"] == volume_id:
                return volume
        return None


if __name__ == "__main__":
    nectar = Nectar()
    images = nectar.list_image()
    print(images)
