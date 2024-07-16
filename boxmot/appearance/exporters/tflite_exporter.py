import os
from boxmot.appearance.exporters.base_exporter import BaseExporter
from boxmot.utils import logger as LOGGER


class TFLiteExporter(BaseExporter):
    required_packages = (
        "onnx2tf>=1.18.0", 
        "tensorflow",
        "tf_keras",  # required by 'onnx2tf' package
        "sng4onnx>=1.0.1",  # required by 'onnx2tf' package
        "onnx_graphsurgeon>=0.3.26",  # required by 'onnx2tf' package
        "onnxslim>=0.1.31",
        "onnxruntime",
    )
    cmds = '--extra-index-url https://pypi.ngc.nvidia.com'
    
    def export(self):

        import onnx2tf
        LOGGER.info(f"\nStarting {self.file} export with onnx2tf {onnx2tf.__version__}")
        input_onnx_file_path = str(self.file.with_suffix('.onnx'))
        output_folder_path = input_onnx_file_path.replace(".onnx", f"_saved_model{os.sep}")
        onnx2tf.convert(
            input_onnx_file_path=input_onnx_file_path,
            output_folder_path=output_folder_path,
            not_use_onnxsim=True,
            verbosity=True,
            #output_integer_quantized_tflite=self.args.int8,
            quant_type="per-tensor",  # "per-tensor" (faster) or "per-channel" (slower but more accurate)
            #custom_input_op_name_np_data_path=np_data,
        )
        return output_folder_path
