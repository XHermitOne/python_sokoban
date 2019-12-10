# sudo apt install python3-sphinx
# pip3 install sphinx-epytext
rm --recursive ./doc/api/*.*

# epydoc --debug --fail-on-error --html --graph umlclasstree --output /mnt/defis/defis3/ic/doc ic
# epydoc --debug --html --output /mnt/defis/defis3/ic/doc ic

# ~/.local/bin/sphinx-apidoc --separate --full --doc-project "python_sokoban" --doc-author "Kolchanov Alexander" --doc-version "0.1.1.1" --output-dir ./doc/api ./
sphinx-apidoc --separate --full --doc-project "python_sokoban" --doc-author "Kolchanov Alexander" --doc-version "0.1.1.1" --output-dir ./doc/api ./

# I was running Sphinx under Python 3, thus needed:
# sed -i.bak "s/ python / python3 /g" ./doc/api/Makefile
# Note Bio.Restriction breaks Sphinx, so skip it entirely!
#
# Exception occurred:
#   File ".../site-packages/Bio/Restriction/Restriction.py", line 341, in __len__
#     return cls.size
# AttributeError: type object 'RestrictionType' has no attribute 'size'
#
# rm -rf ./doc/api/ic.Restriction.*
make -C ./doc/api/ html

#cd /mnt/defis/defis3/ic/doc/
# python3 ~/.local/lib/python3.6/site-packages/sphinx/cmd/quickstart.py
# python3 ~/.local/lib/python3.6/site-packages/sphinx/cmd/build.py -a ./ /mnt/defis/defis3/ic/doc
