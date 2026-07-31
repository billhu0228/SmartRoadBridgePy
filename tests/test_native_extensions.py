from pathlib import Path
import shutil

import pytest

from srbpy.alignment.align_pqx import PQX
from srbpy.public.gfunc import intersection_seg_arc, intersection_seg_seg


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_ICD = PROJECT_ROOT / "docs" / "test_data" / "M.ICD"


def test_pqx_reads_path_with_spaces_and_unicode(tmp_path: Path) -> None:
    sample_dir = tmp_path / "中文 路线"
    sample_dir.mkdir()
    sample_path = sample_dir / "测试路线.ICD"
    shutil.copyfile(SAMPLE_ICD, sample_path)

    pqx = PQX(sample_path)

    assert pqx.start_pk == pytest.approx(0.0)
    assert pqx.end_pk == pytest.approx(2497.1123919644933, abs=1e-9)
    assert isinstance(pqx.Text, str)
    assert "785642.8283958518" in pqx.Text

    start = pqx.get_coordinate(pqx.start_pk)
    assert start.X() == pytest.approx(571183.0311021816)
    assert start.Y() == pytest.approx(785642.8283958518)


def test_missing_icd_file_reports_clear_error(tmp_path: Path) -> None:
    missing = tmp_path / "不存在的路线.ICD"

    with pytest.raises(RuntimeError, match="无法打开 ICD 文件"):
        PQX(missing)


def test_public_geometry_extension() -> None:
    assert intersection_seg_seg(
        [0.0, 0.0],
        [2.0, 2.0],
        [0.0, 2.0],
        [2.0, 0.0],
    ) == pytest.approx([1.0, 1.0])

    assert intersection_seg_arc(
        0.0,
        0.0,
        1.0,
        -2.0,
        0.0,
        2.0,
        0.0,
    ) == pytest.approx([1.0, 0.0])
