import os
from modules import paths
from modules.paths_internal import normalized_filepath


def preload(parser):
    parser.add_argument(
        "--drct-models-path",
        type=normalized_filepath,
        help="Path to directory with DRCT model file(s).",
        default=os.path.join(paths.models_path, "DRCT"),
    )
    parser.add_argument(
        "--atd-models-path",
        type=normalized_filepath,
        help="Path to directory with ATD model file(s).",
        default=os.path.join(paths.models_path, "ATD"),
    )
    parser.add_argument(
        "--mosr-models-path",
        type=normalized_filepath,
        help="Path to directory with MoSR model file(s).",
        default=os.path.join(paths.models_path, "MoSR"),
    )
    parser.add_argument(
        "--moesr-models-path",
        type=normalized_filepath,
        help="Path to directory with MoESR model file(s).",
        default=os.path.join(paths.models_path, "MoESR"),
    )
    parser.add_argument(
        "--plksr-models-path",
        type=normalized_filepath,
        help="Path to directory with PLKSR model file(s).",
        default=os.path.join(paths.models_path, "PLKSR"),
    )
    parser.add_argument(
        "--realplksr-models-path",
        type=normalized_filepath,
        help="Path to directory with RealPLKSR model file(s).",
        default=os.path.join(paths.models_path, "RealPLKSR"),
    )
    parser.add_argument(
        "--rcan-models-path",
        type=normalized_filepath,
        help="Path to directory with RCAN model file(s).",
        default=os.path.join(paths.models_path, "RCAN"),
    )
