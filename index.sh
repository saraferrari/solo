if [ "$#" -ne 1 ]; then
  echo "Usage: ./index.sh <dataset>"
  exit
fi
work_dir="$(dirname "$PWD")"
dataset=$1
source ../pyenv/fusion_decoder/bin/activate
python index_tables.py \
--work_dir ${work_dir} \
--dataset ${dataset} \
