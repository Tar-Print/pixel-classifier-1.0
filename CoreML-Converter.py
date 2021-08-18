#Dependencies
import coremltools
from keras.models import load_model

dot_model_model = load_model('Models/wFall-woutWater-Models/Model-6-USE/ML-Model.model')
#['pixel_r','pixel_g','pixel_b','local_r','local_g','local_b','edges_r','edges_g','edges_b'],
your_model = coremltools.converters.keras.convert(dot_model_model,
                                                  class_labels=['dry_pervious', 'fall_pervious', 'norm_impervious',
                                                                'norm_pervious', 'shaded_pervious','tan_impervious'])

your_model.save('Models/wFall-woutWater-Models/Model-6-USE/CoreML-Model.mlmodel')