import zmq

ctx = zmq.Context()

pub = ctx.socket(zmq.XPUB)
pub.bind("tcp://*:5556")

sub = ctx.socket(zmq.XSUB)
sub.bind("tcp://*:5555")

zmq.proxy(pub, sub)

pub.close()
sub.close()
ctx.close()
