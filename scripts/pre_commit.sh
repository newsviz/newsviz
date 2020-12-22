image=newsviz:$(git rev-parse --abbrev-ref HEAD)
docker run --rm -v $(pwd):/code -w /code/ $image pre-commit run --all-files
