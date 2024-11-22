EXAMPLE1=./tests/examples/exmpl1.json
EXAMPLE2=./tests/examples/exmpl2.json
EXAMPLE3=./tests/examples/exmpl3.json
EXAMPLE4=./tests/examples/exmpl4.json
TESTS=./tests/test.py

run:
	python main.py $(file)

example1:
	python main.py $(EXAMPLE1)

example2:
	python main.py $(EXAMPLE2)

example3:
	python main.py $(EXAMPLE3)

example4:
	python main.py $(EXAMPLE4)

examples: 
	echo "Пример №1" 
	make example1
	echo "================================="
	echo "Пример №2\n" 
	make example2
	echo "================================="
	echo "Пример №3\n" 
	make example3
	echo "================================="
	echo "Пример №4\n" 
	make example4
	echo "================================="

test:
	python -m unittest $(TESTS)
