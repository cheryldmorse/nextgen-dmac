import pytest
from ingest_tools.nos_ofs import NOS_Pipeline
from ingest_tools.pipeline import Pipeline, PipelineContext
from ingest_tools.rtofs import RTOFS_Pipeline


# TODO: This is simply a demonstration, but we can make this more robust to automatically test all available pipelines
@pytest.mark.parametrize('test_input', [
    [RTOFS_Pipeline(), 'rtofs.20230922/rtofs_glo_2ds_f001_diag.nc', 'rtofs.20230922.rtofs_glo_2ds_f001_diag.nc.zarr'],
    [NOS_Pipeline(), 'tbofs.20230314/nos.tbofs.fields.n002.20230314.t00z.nc', 'tbofs/nos.tbofs.fields.n002.20230314.t00z.nc.zarr'],
    [NOS_Pipeline(), 'ngofs2/nos.ngofs2.fields.f042.20231003.t09z.nc', 'ngofs2/nos.ngofs2.fields.f042.20231003.t09z.nc.zarr']
    ])
def test_pipelines(test_input):
    pipeline = test_input[0]
    test_key = test_input[1]
    expected_key = test_input[2]

    assert pipeline.accepts(test_key)
    
    filemetadata = pipeline.read_file_metadata(test_key)
    assert filemetadata.output_key == expected_key


def test_pipeline_context():
    context = PipelineContext('us-east-1', 'nextgen-dmac')
    context.add_pipeline('nos', NOS_Pipeline())
    context.add_pipeline('rtofs', RTOFS_Pipeline())

    # This test should only return the NOS Pipeline because that's what this data is
    matching = context.get_matching_pipelines('tbofs.20230314/nos.tbofs.fields.n002.20230314.t00z.nc')
    assert len(matching) == 1
    assert isinstance(matching[0], NOS_Pipeline)


# TODO: Can create a generic function passing in the filemetadata object for validation
def test_filemetadata():
    key = 'cbofs.20231022/nos.cbofs.fields.n006.20231022.t00z.nc'
    pipeline = NOS_Pipeline()
    m = pipeline.read_file_metadata(key)        
    assert m.source_key == key
    assert m.dataset_id == 'cbofs'
    assert m.model_date == '20231022'
    assert m.model_hour == '00'
    assert m.offset == 6
    assert m.output_key == 'cbofs/nos.cbofs.fields.n006.20231022.t00z.nc.zarr'


def test_filemetadata_rtofs():
    key = 'rtofs.20230922/rtofs_glo_2ds_f001_diag.nc'
    pipeline = RTOFS_Pipeline()
    m = pipeline.read_file_metadata(key)        
    assert m.source_key == key
    assert m.dataset_id == 'rtofs'
    # TODO: This is inconsistent with how model_date is represented in NOS
    assert m.model_date == '20230922T01' 
    # TODO: Do we need both hour and offset?
    assert m.model_hour == '1'
    assert m.offset == 1
    assert m.output_key == 'rtofs.20230922.rtofs_glo_2ds_f001_diag.nc.zarr'