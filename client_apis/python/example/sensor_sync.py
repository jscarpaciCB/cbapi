import sys
import struct
import socket
import pprint
import optparse

# in the github repo, cbapi is not in the example directory
sys.path.append('../src/cbapi')

import cbapi

def build_cli_parser():
    parser = optparse.OptionParser(usage="%prog [options]", description="Force a single sensor to sync via the API")

    # for each supported output type, add an option
    #
    parser.add_option("-c", "--cburl", action="store", default=None, dest="server_url",
                      help="CB server's URL.  e.g., http://127.0.0.1 ")
    parser.add_option("-a", "--apitoken", action="store", default=None, dest="token",
                      help="API Token for Carbon Black server")
    parser.add_option("-n", "--no-ssl-verify", action="store_false", default=True, dest="ssl_verify",
                      help="Do not verify server SSL certificate.")
    parser.add_option("-i", "--sensorid", action="store", default=None, dest="sensorid",
                      help="sensor id")

    return parser

def main(argv):
    parser = build_cli_parser()
    opts, args = parser.parse_args(argv)
    if not opts.server_url or not opts.token or not opts.sensorid:
        print "Missing required param; run with --help for usage"
        print "Must specify the sensor id"
        sys.exit(-1)

    # build a cbapi object
    #
    cb = cbapi.CbApi(opts.server_url, token=opts.token, ssl_verify=opts.ssl_verify)

    if cb.sensor(opts.sensorid) is None:
        print "-> No configured sensor found with id %s" % opts.sensorid
    else:
        sensor = cb.sensor(opts.sensorid)
        sensor_id = opts.sensorid
        group_id = sensor['group_id']
        event_log_flush_time = sensor['event_log_flush_time']
        cb.sensor_force_sync(sensor_id, group_id, event_log_flush_time)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))