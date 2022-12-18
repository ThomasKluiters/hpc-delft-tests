import dataclasses
from pathlib import Path
from typing import List, Callable, Tuple, Optional, Union, Iterable

import dask
from dask.delayed import Delayed

from annotator.annotator import Annotator
from common import InputFile
from embedder.core import Embedder

DaskKey = Tuple[str, str]
DaskTask = Tuple[DaskKey, Tuple[Union[Callable, Delayed], Optional[DaskKey]]]
DaskTasks = List[DaskTask]


def identify_target_files(path: Path, extension: str) -> List[InputFile]:
    if not path.exists():
        return []
    if path.is_file():
        if not path.name.endswith(extension):
            return []
        return [InputFile.from_file(path)]
    return list(map(InputFile.from_file, path.rglob(f"*.{extension}")))


@dataclasses.dataclass
class PipelineResult:
    success: bool


@dataclasses.dataclass
class PipelineStep:
    def prepare(self):
        raise NotImplementedError

    def build_tasks_for_keys(self, files: List[InputFile]) -> DaskTasks:
        raise NotImplementedError


@dataclasses.dataclass
class DownloadStep(PipelineStep):
    def prepare(self):
        pass

    def build_tasks_for_keys(self, files: List[DaskKey]) -> DaskTasks:
        return [
            (("collect", "1"), (lambda: 0, None)),
            (("sequence", "1"), (lambda x: 0, ("collect", "1"))),
            (("sequence", "2"), (lambda x: 0, ("collect", "1"))),
            (("sequence", "3"), (lambda x: 0, ("collect", "1"))),
        ]


@dataclasses.dataclass
class AnnotationStep(PipelineStep):
    annotator: Annotator

    def prepare(self):
        self.annotator.configure()

    def build_tasks_for_keys(self, keys: List[DaskKey]) -> DaskTasks:
        return [self.build_task_for_key(key) for key in keys]

    def build_task_for_key(self, key: DaskKey) -> DaskTask:
        return ("protein", key[1]), (self.annotator.annotate_input_file, key)


@dataclasses.dataclass
class EmbedderStep(PipelineStep):
    embedder: Embedder

    def prepare(self):
        self.embedder.configure()

    def build_tasks_for_keys(self, keys: List[DaskKey]) -> DaskTasks:
        return [self.build_task_for_key(key) for key in keys]

    def build_task_for_key(self, key: DaskKey) -> DaskTask:
        return ("embedding", key[1]), (self.embedder.compute_embeddings_for_file, key)


def convert_key_to_string(key: Optional[Union[DaskKey, Iterable[DaskKey]]]):
    if key is None:
        return None
    if isinstance(key, tuple):
        return "-".join(reversed(key))
    return ["-".join(reversed(k)) for k in key]


@dataclasses.dataclass
class Pipeline:
    steps: List[PipelineStep]

    def build_graph(self):
        graph = {}
        keys = []
        for step in self.steps:
            # step.prepare()
            tasks = dict(step.build_tasks_for_keys(keys))
            keys = tasks.keys()
            graph.update({
                convert_key_to_string(k): (task, convert_key_to_string(dep))
                for (k, (task, dep))
                in tasks.items()
            })
        graph['collect'] = (print, list(map(convert_key_to_string, keys)))
        return graph
