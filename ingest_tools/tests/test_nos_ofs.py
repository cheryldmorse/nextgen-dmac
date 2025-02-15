import ingest_tools.nos_ofs as nos_ofs
from ingest_tools.generic import ModelRunType


def test_parse_model_run_datestamp():
    # ROMS fields forecast
    key = 'nos/dbofs/nos.dbofs.fields.f001.20230315.t00z.nc.zarr'
    model_date, model_hour = nos_ofs.parse_nos_model_run_datestamp(key)
    assert model_date == '20230315'
    assert model_hour == '00'

    # ROMS fields nowcast
    key = 'nos/dbofs/nos.dbofs.fields.n001.20231019.t06z.nc.zarr'
    model_date, model_hour = nos_ofs.parse_nos_model_run_datestamp(key)
    assert model_date == '20231019'
    assert model_hour == '06'

    # FVCOM fields
    key = 'nos/ngofs2/nos.ngofs2.fields.f042.20231003.t09z.nc.zarr'
    model_date, model_hour = nos_ofs.parse_nos_model_run_datestamp(key)
    assert model_date == '20231003'
    assert model_hour == '09'

    # FVCOM 2D
    key = 'nos/ngofs2/nos.ngofs2.2ds.f040.20231003.t03z.nc.zarr'
    model_date, model_hour = nos_ofs.parse_nos_model_run_datestamp(key)
    assert model_date == '20231003'
    assert model_hour == '03'


def test_parse_model_run_datestamp_offset():
    # ROMS fields forecast
    key = 'nos/dbofs/nos.dbofs.fields.f001.20230315.t00z.nc.zarr'
    model_date, offset = nos_ofs.parse_nos_model_run_datestamp_offset(key)
    assert model_date == '20230315T01'
    assert offset == 1

    # ROMS fields nowcast
    key = 'nos/dbofs/nos.dbofs.fields.n001.20231019.t06z.nc.zarr'
    model_date, offset = nos_ofs.parse_nos_model_run_datestamp_offset(key)
    assert model_date == '20231019T07'
    assert offset == 1

    # FVCOM fields forecast
    key = 'nos/ngofs2/nos.ngofs2.fields.f042.20231003.t09z.nc.zarr'
    model_date, offset = nos_ofs.parse_nos_model_run_datestamp_offset(key)
    assert model_date == '20231005T03'
    assert offset == 42

    # FVCOM 2D forecasts
    key = 'nos/ngofs2/nos.ngofs2.2ds.f040.20231003.t03z.nc.zarr'
    model_date, offset = nos_ofs.parse_nos_model_run_datestamp_offset(key)
    assert model_date == '20231004T19'
    assert offset == 40


def test_generate_model_run_glob_expression():
    # ROMS fields forecast
    key = 'nos/dbofs/nos.dbofs.fields.f001.20230315.t00z.nc.zarr'
    model_date, model_hour = nos_ofs.parse_nos_model_run_datestamp(key)
    glob_expression, run_type = nos_ofs.generate_nos_model_run_glob_expression(key, model_date, model_hour)
    assert glob_expression == 'nos/dbofs/nos.dbofs.fields.f*.20230315.t00z.nc.zarr'
    assert run_type == nos_ofs.ModelRunType.FORECAST

    # ROMS fields nowcast
    key = 'nos/dbofs/nos.dbofs.fields.n001.20230315.t00z.nc.zarr'
    model_date, model_hour = nos_ofs.parse_nos_model_run_datestamp(key)
    glob_expression, run_type = nos_ofs.generate_nos_model_run_glob_expression(key, model_date, model_hour)
    assert glob_expression == 'nos/dbofs/nos.dbofs.fields.n*.20230315.t00z.nc.zarr'
    assert run_type == nos_ofs.ModelRunType.NOWCAST

    # FVCOM fields forecast
    key = 'nos/ngofs2/nos.ngofs2.fields.f042.20231003.t09z.nc.zarr'
    model_date, model_hour = nos_ofs.parse_nos_model_run_datestamp(key)
    glob_expression, run_type = nos_ofs.generate_nos_model_run_glob_expression(key, model_date, model_hour)
    assert glob_expression == 'nos/ngofs2/nos.ngofs2.fields.f*.20231003.t09z.nc.zarr'
    assert run_type == nos_ofs.ModelRunType.FORECAST


def test_generate_best_time_series_glob_expression():
    # ROMS fields forecast
    key = 'nos/dbofs/nos.dbofs.fields.f001.20230315.t00z.nc.zarr'
    glob_expression = nos_ofs.generate_nos_best_time_series_glob_expression(key)
    assert glob_expression == 'nos/dbofs/nos.dbofs.fields.f*.*.t*z.nc.zarr'

    # FVCOM fields forecast
    key = 'nos/ngofs2/nos.ngofs2.fields.f042.20231003.t09z.nc.zarr'
    glob_expression = nos_ofs.generate_nos_best_time_series_glob_expression(key)
    assert glob_expression == 'nos/ngofs2/nos.ngofs2.fields.f*.*.t*z.nc.zarr'
