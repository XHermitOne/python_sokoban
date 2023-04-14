rm --recursive ./doc/api/*.*
sphinx-apidoc --separate --full --doc-project "python_sokoban" --doc-author "Kolchanov Alexander" --doc-version "0.1.1.1" --output-dir ./doc/api ./
make -C ./doc/api/ html
