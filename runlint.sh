
# |  xargs 
for x in `find src -name \*.py`;
do echo $x;
    PYTHONPATH=src ~/.local/bin/pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" $x
done

