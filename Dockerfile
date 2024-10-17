FROM public.ecr.aws/lambda/python:3.10

COPY app ${LAMBDA_TASK_ROOT}

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD [ "main.handler" ]