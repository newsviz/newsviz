image=newsviz:$(git rev-parse --abbrev-ref HEAD)
docker run --rm -v $(pwd):/code -w /code/newsviz -p 8080:8080 $image python -m visualizer.app
