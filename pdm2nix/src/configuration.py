import pdm
from pdm.project.lockfile import Lockfile
import toml

from resolvelib.reporters import BaseReporter
from pdm.core import Project, Core
from pdm.resolver import resolve
from pdm.models.requirements import Requirement
from pdm.cli.utils import fetch_hashes
from pdm.cli.filters import GroupSelection
from pdm.environments.local import PythonLocalEnvironment

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def resolve_from_lockfile(pdm_project: Project, requirements: list[Requirement]):
    resolve_max_rounds = int(pdm_project.config["strategy.resolve_max_rounds"])
    print(pdm_project.environment.marker_environment)
    reqs = [
        req for req in requirements if not req.marker or req.marker.evaluate(pdm_project.environment.marker_environment)
    ]
    reporter = BaseReporter()
    provider = pdm_project.get_provider(for_install=True)
    resolver: Resolver = pdm_project.core.resolver_class(provider, reporter)
    mapping, *_ = resolve(
        resolver,
        reqs,
        pdm_project.environment.python_requires,
        resolve_max_rounds,
    )
    fetch_hashes(provider.repository, mapping)
    return mapping

def generate_configuration(project_path: str, group: str) -> None:
    pdm_project = Core().create_project(project_path, is_global=False)
    selection = GroupSelection(project=pdm_project, group=group)
    selection.validate()

    requirements = list()
    for group in selection:
        requirements.extend(pdm_project.get_dependencies(group).values())
    candidates = resolve_from_lockfile(pdm_project, requirements)

    synchronizer = pdm_project.core.synchronizer_class(
        candidates,
        pdm_project.environment,
        clean=False,
        dry_run=False,
        no_editable=False,
        install_self="default" in selection and bool(pdm_project.name),
        reinstall=True,
        only_keep=False,
        fail_fast=False,
    )
    to_add, to_update, to_remove = synchronizer.compare_with_working_set()

    for a in to_add:
        candidates[a].prepare(pdm_project.environment)
        print(str(candidates[a]))
        candidates[a]._prepared.obtain(allow_all=True)
        print(candidates[a]._prepared.link, candidates[a].hashes[candidates[a]._prepared.link])

















