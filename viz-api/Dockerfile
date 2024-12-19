FROM continuumio/miniconda3:4.8.2 AS base
WORKDIR /taswira
COPY environment.yml .
RUN conda update conda \
      && conda install "conda=4.8.3" \
      && conda env create -f environment.yml \
      && conda clean -afy
ENV CONDA_ENV=/opt/conda/envs/taswira
ENV PATH="$CONDA_ENV/bin:$PATH"
COPY . .

SHELL ["conda", "run", "-n", "taswira", "/bin/bash", "-c"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "2", "--timeout", "0", "app:app"]