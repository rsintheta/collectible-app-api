# I spent a lot of time learning about how to obfuscate my django secret key, 
# and I've implemented such features for this project, however, I haven't yet
# discovered a way to communicate with travis-ci/docker this key easily.

# My three ideas were 
#   1) A seperate private github repo that I could pull the variable from
#   2) Adding it as an environment variable to travis-ci/docker
#   3) A seperate django project that accepts get requests for the key.

# However, for the sake of travis-ci, and so this little red 'X' will stop 
# showing up on my beautiful repository, I will include a randomly generated 
# secret key here. I will create a fork of this version when I decide to 
# deploy to AWS which does not have this file, securely handles the secret key.

# I'll say it again, I didn't want it to be this way, 
# but until I dig deeper down this rabbit hole, travis-ci has forced my hand.

keyOut = '%=jqsz=b_8=$iow&#(5@-qt66!t@%p4l#4=)ue14_7gm65jv-c'
