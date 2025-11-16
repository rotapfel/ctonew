import pytest
import numpy as np
import json
import csv
from pathlib import Path
import tempfile
from rb_eit import (
    DoubleLambdaSystem,
    FWMSpectraCalculator,
    ParameterSweep,
    ParameterSweepResult,
    SpectraExporter
)


class TestSpectraExporterCSV:
    
    @pytest.fixture
    def result_1d(self):
        param_values = np.linspace(-10e6, 10e6, 20) * 2 * np.pi
        chi3_values = np.random.randn(20) + 1j * np.random.randn(20)
        intensity_values = np.abs(chi3_values)**2
        
        return ParameterSweepResult(
            parameter_name='probe_detuning',
            parameter_values=param_values,
            chi3_values=chi3_values,
            intensity_values=intensity_values,
            fixed_parameters={'pump_rabi': 2 * np.pi * 10e6},
            metadata={'units': 'rad/s'}
        )
    
    @pytest.fixture
    def result_2d(self):
        param1_values = np.linspace(-5e6, 5e6, 10) * 2 * np.pi
        param2_values = np.linspace(5e6, 15e6, 8) * 2 * np.pi
        chi3_values = np.random.randn(10, 8) + 1j * np.random.randn(10, 8)
        intensity_values = np.abs(chi3_values)**2
        
        return ParameterSweepResult(
            parameter_name='probe_detuning',
            parameter_values=param1_values,
            secondary_parameter_name='pump_rabi',
            secondary_parameter_values=param2_values,
            chi3_values=chi3_values,
            intensity_values=intensity_values,
            fixed_parameters={'number_density': 1e17},
            metadata={'sweep_type': '2D'}
        )
    
    def test_export_csv_1d(self, result_1d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_output.csv"
            SpectraExporter.to_csv(result_1d, str(filepath))
            
            assert filepath.exists()
            
            with open(filepath, 'r') as f:
                lines = f.readlines()
                assert len(lines) > 20
                assert '# Export Timestamp:' in lines[0]
                assert '# Parameter: probe_detuning' in lines[1]
    
    def test_export_csv_1d_without_metadata(self, result_1d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_output.csv"
            SpectraExporter.to_csv(result_1d, str(filepath), include_metadata=False)
            
            assert filepath.exists()
            
            with open(filepath, 'r') as f:
                lines = f.readlines()
                assert not lines[0].startswith('#')
    
    def test_csv_1d_data_integrity(self, result_1d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_output.csv"
            SpectraExporter.to_csv(result_1d, str(filepath))
            
            data_rows = []
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row[0].startswith('#'):
                        data_rows.append(row)
            
            header = data_rows[0]
            assert 'probe_detuning' in header
            assert 'chi3_real' in header
            assert 'chi3_imag' in header
            assert 'chi3_magnitude' in header
            assert 'fwm_intensity' in header
            
            assert len(data_rows) == 21
    
    def test_export_csv_2d(self, result_2d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_2d_output.csv"
            SpectraExporter.to_csv(result_2d, str(filepath))
            
            assert filepath.exists()
            
            with open(filepath, 'r') as f:
                lines = f.readlines()
                assert '# Secondary Parameter: pump_rabi' in lines[2]
    
    def test_csv_2d_data_integrity(self, result_2d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_2d_output.csv"
            SpectraExporter.to_csv(result_2d, str(filepath))
            
            data_rows = []
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and not row[0].startswith('#'):
                        data_rows.append(row)
            
            header = data_rows[0]
            assert len(header) == 7
            
            assert len(data_rows) == 81


class TestSpectraExporterJSON:
    
    @pytest.fixture
    def result_1d(self):
        param_values = np.linspace(-10e6, 10e6, 20) * 2 * np.pi
        chi3_values = np.random.randn(20) + 1j * np.random.randn(20)
        intensity_values = np.abs(chi3_values)**2
        
        return ParameterSweepResult(
            parameter_name='probe_detuning',
            parameter_values=param_values,
            chi3_values=chi3_values,
            intensity_values=intensity_values,
            fixed_parameters={'pump_rabi': 2 * np.pi * 10e6},
            metadata={'units': 'rad/s'}
        )
    
    @pytest.fixture
    def result_2d(self):
        param1_values = np.linspace(-5e6, 5e6, 10) * 2 * np.pi
        param2_values = np.linspace(5e6, 15e6, 8) * 2 * np.pi
        chi3_values = np.random.randn(10, 8) + 1j * np.random.randn(10, 8)
        intensity_values = np.abs(chi3_values)**2
        
        return ParameterSweepResult(
            parameter_name='probe_detuning',
            parameter_values=param1_values,
            secondary_parameter_name='pump_rabi',
            secondary_parameter_values=param2_values,
            chi3_values=chi3_values,
            intensity_values=intensity_values,
            fixed_parameters={'number_density': 1e17},
            metadata={'sweep_type': '2D'}
        )
    
    def test_export_json_1d(self, result_1d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_output.json"
            SpectraExporter.to_json(result_1d, str(filepath))
            
            assert filepath.exists()
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert 'metadata' in data
            assert 'parameter' in data
            assert 'results' in data
    
    def test_json_1d_structure(self, result_1d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_output.json"
            SpectraExporter.to_json(result_1d, str(filepath))
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert data['parameter']['name'] == 'probe_detuning'
            assert len(data['parameter']['values']) == 20
            assert 'chi3' in data['results']
            assert 'real' in data['results']['chi3']
            assert 'imag' in data['results']['chi3']
            assert 'magnitude' in data['results']['chi3']
            assert 'phase' in data['results']['chi3']
            assert 'fwm_intensity' in data['results']
    
    def test_json_1d_metadata(self, result_1d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_output.json"
            SpectraExporter.to_json(result_1d, str(filepath))
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert 'timestamp' in data['metadata']
            assert data['metadata']['parameter_name'] == 'probe_detuning'
            assert data['metadata']['num_points'] == 20
            assert data['metadata']['sweep_type'] == '1D'
    
    def test_export_json_2d(self, result_2d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_2d_output.json"
            SpectraExporter.to_json(result_2d, str(filepath))
            
            assert filepath.exists()
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert 'secondary_parameter' in data
            assert data['metadata']['sweep_type'] == '2D'
    
    def test_json_2d_structure(self, result_2d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_2d_output.json"
            SpectraExporter.to_json(result_2d, str(filepath))
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert data['secondary_parameter']['name'] == 'pump_rabi'
            assert len(data['secondary_parameter']['values']) == 8
            assert len(data['results']['chi3']['real']) == 10
            assert len(data['results']['chi3']['real'][0]) == 8
    
    def test_from_json_1d(self, result_1d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_output.json"
            SpectraExporter.to_json(result_1d, str(filepath))
            
            loaded_data = SpectraExporter.from_json(str(filepath))
            
            assert 'metadata' in loaded_data
            assert 'parameter' in loaded_data
            assert 'results' in loaded_data
            assert isinstance(loaded_data['parameter']['values'], np.ndarray)
            assert 'chi3_complex' in loaded_data['results']
            assert loaded_data['results']['chi3_complex'].dtype == complex
    
    def test_from_json_2d(self, result_2d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_2d_output.json"
            SpectraExporter.to_json(result_2d, str(filepath))
            
            loaded_data = SpectraExporter.from_json(str(filepath))
            
            assert 'secondary_parameter' in loaded_data
            assert isinstance(
                loaded_data['secondary_parameter']['values'],
                np.ndarray
            )
    
    def test_roundtrip_1d(self, result_1d):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_output.json"
            SpectraExporter.to_json(result_1d, str(filepath))
            loaded_data = SpectraExporter.from_json(str(filepath))
            
            assert np.allclose(
                loaded_data['parameter']['values'],
                result_1d.parameter_values
            )
            assert np.allclose(
                loaded_data['results']['chi3_complex'],
                result_1d.chi3_values
            )
            assert np.allclose(
                loaded_data['results']['fwm_intensity'],
                result_1d.intensity_values
            )


class TestExportMultipleFormats:
    
    @pytest.fixture
    def result(self):
        param_values = np.linspace(-10e6, 10e6, 15) * 2 * np.pi
        chi3_values = np.random.randn(15) + 1j * np.random.randn(15)
        intensity_values = np.abs(chi3_values)**2
        
        return ParameterSweepResult(
            parameter_name='probe_detuning',
            parameter_values=param_values,
            chi3_values=chi3_values,
            intensity_values=intensity_values
        )
    
    def test_export_multiple_formats(self, result):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir) / "test_output"
            filepaths = SpectraExporter.export_multiple_formats(
                result,
                str(base_path)
            )
            
            assert 'csv' in filepaths
            assert 'json' in filepaths
            assert Path(filepaths['csv']).exists()
            assert Path(filepaths['json']).exists()
    
    def test_export_csv_only(self, result):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir) / "test_output"
            filepaths = SpectraExporter.export_multiple_formats(
                result,
                str(base_path),
                formats=['csv']
            )
            
            assert 'csv' in filepaths
            assert 'json' not in filepaths
    
    def test_export_json_only(self, result):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir) / "test_output"
            filepaths = SpectraExporter.export_multiple_formats(
                result,
                str(base_path),
                formats=['json']
            )
            
            assert 'json' in filepaths
            assert 'csv' not in filepaths


class TestIntegrationWithRealData:
    
    def test_full_workflow_export(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        calculator = FWMSpectraCalculator(system)
        sweep = ParameterSweep(calculator)
        
        result = sweep.sweep_probe_detuning(
            probe_detuning_min=-10e6 * 2 * np.pi,
            probe_detuning_max=10e6 * 2 * np.pi,
            num_points=30
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir) / "fwm_spectrum"
            filepaths = SpectraExporter.export_multiple_formats(result, str(base_path))
            
            assert Path(filepaths['csv']).exists()
            assert Path(filepaths['json']).exists()
            
            loaded_data = SpectraExporter.from_json(filepaths['json'])
            assert len(loaded_data['parameter']['values']) == 30
    
    def test_2d_sweep_export(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        calculator = FWMSpectraCalculator(system)
        sweep = ParameterSweep(calculator)
        
        probe_detuning_values = np.linspace(-5e6, 5e6, 12) * 2 * np.pi
        pump_rabi_values = np.linspace(5e6, 15e6, 10) * 2 * np.pi
        
        result = sweep.sweep_2d(
            param1_name='probe_detuning',
            param1_values=probe_detuning_values,
            param2_name='pump_rabi',
            param2_values=pump_rabi_values
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "fwm_2d.json"
            SpectraExporter.to_json(result, str(filepath))
            
            assert filepath.exists()
            
            loaded_data = SpectraExporter.from_json(str(filepath))
            assert loaded_data['results']['chi3_complex'].shape == (12, 10)
