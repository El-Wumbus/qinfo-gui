pythonfiles = $(wildcard ./src/*.py)

default: compiled-package

package: clean
	python3 setup.py sdist bdist_wheel

install: package
	sh -c "pip install dist/*.whl"

upload: package
	twine upload dist/*

clean:
	rm -rf src/__pycache__ dist build	
