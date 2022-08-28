default: compiled-package

package: clean
	
install: package
	python3 setup.py sdist bdist_wheel
	sh -c "pip -r install dist/*.whl"

upload: package
	twine upload dist/*

clean:
	rm -rf src/__pycache__ dist build	
