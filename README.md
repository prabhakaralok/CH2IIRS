# CH2IIRS
Chandrayaan 2 Level 2 IIRS data processing.
This plugin performs Thermal correction, Phase correction in the radiance data of Imaging Infrared Spectrometer (IIRS) sensor of Chandrayaan 2. </br>Algorithm of the plugin for thermal correction can be found at <a href="https://www.sciencedirect.com/science/article/abs/pii/S0019103522001853"> Verma, P. A., Chauhan, M., & Chauhan, P. (2022). Lunar surface temperature estimation and thermal emission correction using Chandrayaan-2 imaging infrared spectrometer data for H2O & OH detection using 3 μm hydration feature. Icarus, 383, 115075 </a>.</br>
</br>Algorithm of the plugin for phase correction can be found at <a href="https://onlinelibrary.wiley.com/doi/full/10.1111/maps.70037"> Chauhan, M., Verma, P. A., & Chauhan, P. (2025). Level‐2 processing of Chandrayaan‐2 Imaging Infrared Spectrometer (IIRS) data for generation of surface reflectance. Meteoritics & Planetary Science, 60(9), 2269-2282. </a></br>

<b>Nomenclature of files:</b>
<br>input_filename_phase: Reflectance Corrected for Phase, Incidence angle and Thermal
<br>input_filename_inc_corrRef: Reflectance Corrected for Incidence angle and Thermal
<br>input_filename_corrRef: Reflectance Corrected for Thermal
<br>input_filename_Temp: Temperature
<br>input_filename_angle: Incidence angle</br>

Radiance image of IIRS and solar flux are the input for this plugin. However, solar flux is optional input. All the inputs should be corresponding to all 256 bands of IIRS. <b> This tool works for dark corrected radiance data i.e. file name shall be ch2_iir_nci_xxxxxxxxxxxxxxxxxxx_d_img_xxx</b>
</br>
</br>
<b> One of the there radio buttons need to be selected: </b>
</br>
<ul>Thermal Correction: 
<ul><li> Performs only thermal correction </li>
  <li>Thermally corrected reflectance and temperature files will be created, named as <i>input_filename_corrRef</i> and <i>input_filename_Temp</i> respectively. </li>
  <li>Tool will work for any spatial subset of radiance image also.</li></ul></ul>
</br>
<ul>Indcidence angle: 
  <ul><li>Creates incidence angle image</li>
 <li> Angle file having name <i>input_filename_angle</i> will be created </li>
<li>Tool will work for entire scence only. </li>
<li><b>Note: Input file as well as other supporting files must be in the folder structure of ISSDC </b></li></ul></ul>
</br>
<ul>Thermal and Incidence angle correction: 
<ul> <li> Performs correction for temperature as well as incidence angle</li>
 <li> Tool will work for entire scence only.</li>
  <li>Thermally and incidence angle corrected reflectance, temperature, incidence angle will be the outputs and <i>input_filename_inc_corrRef</i>, <i>input_filename_Temp</i>, <i>input_filename_angle</i> files will be created respectively.</li>
  <li><b>Note: Input file as well as other supporting files must be in the folder structure of ISSDC</b></li></ul></ul>
<ul>Phase Correction:
  <ul><li>Performs correction for temperature, incidence as well as phase angle </li> 
  <li> This tool will work for entire scene only.</li>
  <li>Phase angle, Thermally and incidence angle corrected reflectance, temperature, incidence angle will be the outputs and <i>input_filename_inc_Phase</i>, <i>input_filename_inc_corrRef</i>, <i>input_filename_Temp</i>, <i>input_filename_angle</i> files will be created respectively.</li>
  <li><b>Note: Input file as well as other supporting files must be in the folder structure of ISSDC</b></li>  </ul></ul>
<ul>Temperature:
  <ul><li>Generates Lunar Surface Temperature image </li> 
  <li> This tool will work for any spatial subset of radiance image also.</li>
  <li>Temperature image will be the output and <i>input_filename_Temp</i> file will be created.</li> </ul></ul>
