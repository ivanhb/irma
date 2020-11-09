PARAMS=$@
BASEDIR=$(dirname "$0")
source  $BASEDIR/_venv/bin/activate
python $BASEDIR/run.py $PARAMS
