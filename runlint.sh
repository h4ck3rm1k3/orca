
# |  xargs 
for x in `cat files.txt`;
do echo $x;
    PYTHONPATH=src ~/.local/bin/pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" $x
done

