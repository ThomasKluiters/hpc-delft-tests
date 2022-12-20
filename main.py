from dask_jobqueue import SLURMCluster
from distributed import Client

from annotator.prodigal import ProdigalAnnotator
from embedder.bert import ProteinBertEmbedder
from pipeline.pipeline import EmbedderStep, AnnotationStep, DownloadStep, Pipeline

quality_of_service = "short"
partition = "general"
time = "4:00:00"

cluster = SLURMCluster(
    cores=1,
    processes=1,
    queue="tmkluiters",
    memory="16 GB",
    job_extra_directives=[
        f'--qos="{quality_of_service}"',
        f'--partition={partition}',
        f'--time={time}',
        f'--gres={"gpu"}',
    ],
    scheduler_options={'dashboard_address':'44444'}
)
cluster.scale(16)
client = Client(cluster)

if __name__ == '__main__':
    pipeline = Pipeline([
        DownloadStep("PRJNA555636"),
        AnnotationStep(ProdigalAnnotator()),
        EmbedderStep(ProteinBertEmbedder())
    ])
    graph = pipeline.build_graph()
    print(client.dashboard_link)
    client.get(graph, ['collect'])
