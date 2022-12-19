import dask
from dask_jobqueue import SLURMCluster
from distributed import Client

from annotator.prodigal import ProdigalAnnotator
from embedder.bert import ProteinBertEmbedder
from pipeline.pipeline import EmbedderStep, AnnotationStep, DownloadStep, Pipeline

quality_of_service = "short"
partition = "general"
time = "0:10:00"

cluster = SLURMCluster(
    cores=1,
    processes=1,
    queue="tmkluiters",
    memory="32 GB",
    job_extra_directives=[
        f'--qos="{quality_of_service}"',
        f'--partition={partition}',
        f'--time={time}',
        f'--gres={"gpu:turing:1"}'
    ],
)
cluster.scale(8)
client = Client(cluster)


if __name__ == '__main__':
    pipeline = Pipeline([
        DownloadStep("PRJNA555636"),
        AnnotationStep(ProdigalAnnotator()),
        EmbedderStep(ProteinBertEmbedder.load_model())
    ])
    graph = pipeline.build_graph()
    client.get(graph, ['collect'])
