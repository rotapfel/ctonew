import json
import csv
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from .parameter_sweep import ParameterSweepResult


class SpectraExporter:
    """
    Exporter for FWM spectra data to CSV and JSON formats.
    """
    
    @staticmethod
    def to_csv(
        result: ParameterSweepResult,
        filepath: str,
        include_metadata: bool = True
    ) -> None:
        """
        Export parameter sweep results to CSV file.
        
        Parameters
        ----------
        result : ParameterSweepResult
            Parameter sweep results to export
        filepath : str
            Output file path
        include_metadata : bool, optional
            Whether to include metadata as comments, default True
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', newline='') as f:
            if include_metadata:
                metadata = SpectraExporter._build_metadata(result)
                f.write(f"# Export Timestamp: {metadata['timestamp']}\n")
                f.write(f"# Parameter: {result.parameter_name}\n")
                
                if result.secondary_parameter_name:
                    f.write(f"# Secondary Parameter: {result.secondary_parameter_name}\n")
                
                f.write("# Fixed Parameters:\n")
                for key, value in result.fixed_parameters.items():
                    f.write(f"#   {key}: {value}\n")
                
                f.write("# Metadata:\n")
                for key, value in result.metadata.items():
                    f.write(f"#   {key}: {value}\n")
                f.write("#\n")
            
            writer = csv.writer(f)
            
            if result.secondary_parameter_name is None:
                writer.writerow([
                    result.parameter_name,
                    'chi3_real',
                    'chi3_imag',
                    'chi3_magnitude',
                    'chi3_phase',
                    'fwm_intensity'
                ])
                
                for i, param_val in enumerate(result.parameter_values):
                    chi3 = result.chi3_values[i]
                    intensity = result.intensity_values[i]
                    
                    writer.writerow([
                        param_val,
                        chi3.real,
                        chi3.imag,
                        abs(chi3),
                        np.angle(chi3),
                        intensity
                    ])
            else:
                writer.writerow([
                    result.parameter_name,
                    result.secondary_parameter_name,
                    'chi3_real',
                    'chi3_imag',
                    'chi3_magnitude',
                    'chi3_phase',
                    'fwm_intensity'
                ])
                
                for i, val1 in enumerate(result.parameter_values):
                    for j, val2 in enumerate(result.secondary_parameter_values):
                        chi3 = result.chi3_values[i, j]
                        intensity = result.intensity_values[i, j]
                        
                        writer.writerow([
                            val1,
                            val2,
                            chi3.real,
                            chi3.imag,
                            abs(chi3),
                            np.angle(chi3),
                            intensity
                        ])
    
    @staticmethod
    def to_json(
        result: ParameterSweepResult,
        filepath: str,
        indent: int = 2
    ) -> None:
        """
        Export parameter sweep results to JSON file.
        
        Parameters
        ----------
        result : ParameterSweepResult
            Parameter sweep results to export
        filepath : str
            Output file path
        indent : int, optional
            JSON indentation level, default 2
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = SpectraExporter._build_metadata(result)
        
        data = {
            'metadata': metadata,
            'parameter': {
                'name': result.parameter_name,
                'values': result.parameter_values.tolist(),
                'units': result.metadata.get('units', 'N/A')
            },
            'fixed_parameters': SpectraExporter._serialize_dict(
                result.fixed_parameters
            ),
            'results': {
                'chi3': {
                    'real': np.real(result.chi3_values).tolist(),
                    'imag': np.imag(result.chi3_values).tolist(),
                    'magnitude': np.abs(result.chi3_values).tolist(),
                    'phase': np.angle(result.chi3_values).tolist()
                },
                'fwm_intensity': result.intensity_values.tolist()
            }
        }
        
        if result.secondary_parameter_name is not None:
            data['secondary_parameter'] = {
                'name': result.secondary_parameter_name,
                'values': result.secondary_parameter_values.tolist()
            }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent)
    
    @staticmethod
    def from_json(filepath: str) -> Dict[str, Any]:
        """
        Load parameter sweep results from JSON file.
        
        Parameters
        ----------
        filepath : str
            Input file path
        
        Returns
        -------
        data : Dict[str, Any]
            Loaded data dictionary
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        data['parameter']['values'] = np.array(data['parameter']['values'])
        
        if 'secondary_parameter' in data:
            data['secondary_parameter']['values'] = np.array(
                data['secondary_parameter']['values']
            )
        
        chi3_real = np.array(data['results']['chi3']['real'])
        chi3_imag = np.array(data['results']['chi3']['imag'])
        data['results']['chi3_complex'] = chi3_real + 1j * chi3_imag
        
        data['results']['fwm_intensity'] = np.array(
            data['results']['fwm_intensity']
        )
        
        return data
    
    @staticmethod
    def _build_metadata(result: ParameterSweepResult) -> Dict[str, Any]:
        """Build metadata dictionary."""
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'parameter_name': result.parameter_name,
            'num_points': len(result.parameter_values)
        }
        
        if result.secondary_parameter_name:
            metadata['secondary_parameter_name'] = result.secondary_parameter_name
            metadata['num_secondary_points'] = len(result.secondary_parameter_values)
            metadata['sweep_type'] = '2D'
        else:
            metadata['sweep_type'] = '1D'
        
        metadata.update(result.metadata)
        
        return metadata
    
    @staticmethod
    def _serialize_dict(d: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize dictionary values for JSON export."""
        serialized = {}
        for key, value in d.items():
            if isinstance(value, np.ndarray):
                serialized[key] = value.tolist()
            elif isinstance(value, (np.integer, np.floating)):
                serialized[key] = float(value)
            elif isinstance(value, complex):
                serialized[key] = {'real': value.real, 'imag': value.imag}
            else:
                serialized[key] = value
        return serialized
    
    @staticmethod
    def export_multiple_formats(
        result: ParameterSweepResult,
        base_filepath: str,
        formats: list = None
    ) -> Dict[str, str]:
        """
        Export results to multiple formats.
        
        Parameters
        ----------
        result : ParameterSweepResult
            Parameter sweep results to export
        base_filepath : str
            Base file path (without extension)
        formats : list, optional
            List of formats to export ('csv', 'json'), default both
        
        Returns
        -------
        filepaths : Dict[str, str]
            Dictionary mapping format to output filepath
        """
        if formats is None:
            formats = ['csv', 'json']
        
        filepaths = {}
        
        if 'csv' in formats:
            csv_path = f"{base_filepath}.csv"
            SpectraExporter.to_csv(result, csv_path)
            filepaths['csv'] = csv_path
        
        if 'json' in formats:
            json_path = f"{base_filepath}.json"
            SpectraExporter.to_json(result, json_path)
            filepaths['json'] = json_path
        
        return filepaths
