from __future__ import absolute_import, print_function
import os, sys, time, types, subprocess, signal, logging
from gi.repository import GLib
import pydbus

#
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

def start_network():
	net=iphone['org.bluez.Network1']
	net.Connect('nap')

def device_state_changed(property_dict):
	device_connected = property_dict['Connected']
	
	if device_connected:
		print('Device connected, starting network')
		start_network()
	else:
		log.debug("device disconnected")
	

def network_state_changed(property_dict):
	log.debug('Network State Changed: %s', property_dict)
	
	
# DBUS Callback
def properties_changed(interface, property_dict, unused_aray):
	"""
	Called when properties for the bluez stack change
	"""
	log.debug('Interface: %s :: Property_dict: %s', interface, property_dict) 
	 
	if interface == 'org.bluez.Device1': 
		device_state_changed(property_dict)
	elif interface == 'org.bluez.Network1': 
		network_state_changed(property_dict)
	else: 
		log.debug('Unhandled DBUS interface: %s :: Property_dict: %s', interface, property_dict) 


def main():
	import argparse
	parser = argparse.ArgumentParser(description='Connect Pi to phone')
	parser.add_argument('remote_addr', help='Remote device address to connect to.')
	opts = parser.parse_args()
	remote_addr = opts.remote_addr

	bus = pydbus.SystemBus()
	global iphone
	iphone = bus.get('org.bluez','/org/bluez/hci0/dev_{}'.format(remote_addr.replace(':','_')))
	iphone.PropertiesChanged.connect(properties_changed)
	loop = GLib.MainLoop()
	loop.run()


if __name__ == '__main__': sys.exit(main())