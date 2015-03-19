# Creating configurations with `randconfig`

# Invalid configurations

Sometimes, `make randconfig` will create an invalid configuration. Actually, 
it turnes out, that approximately 25% of the configurations are invalid. Out
of 1701 configurations, that was randomly created, 391 of them had one or more
warnings. See table 1.

  nu warn  |  nu confs
 ======================
     0     |   1310
     1     |    274
     2     |     96
     3     |     20
     4     |      1
 ----------------------
   total   |   1701


Table 1: Shows the distribution of errors in the configurations

When looking at the warnings, it turns out, it is the same 9 warnings that are
repeatedly showing up. See table 2.


  wrn | selected                           | selects          | unmet depends
 =============================================================================
  216 | SND_SOC_INTEL_BYTCR_RT5640_MACH && | SND_SST_IPC_ACPI | SOUND && 
      | SND_SOC_INTEL_CHT_BSW_RT5672_MACH  |                  | !M68K && 
      |                                    |                  | !UML && 
      |                                    |                  | SND && 
      |                                    |                  | SND_SOC && 
      |                                    |                  | ACPI
      |                                    |                  |    
  149 | USB_OTG_FSM &&                     | USB_OTG          | USB_SUPPORT &&
      | FSL_USB2_OTG &&                    |                  | USB &&   
      | USB_MV_OTG                         |                  | PM   
      |                                    |                  |    
   70 | VIDEO_TIMBERDALE                   | TIMB_DMA         | DMADEVICES &&
      |                                    |                  | MFD_TIMBERDALE
      |                                    |                  |    
   27 | DRM_RADEON &&                      | BACKLIGHT_CLASS_DEVICE | HAS_IOMEM &&
      | DRM_NOUVEAU &&                     |                  | BACKLIGHT_LCD_SUPPORT
      | DRM_I915 && 
      | DRM_GMA500 && 
      | DRM_SHMOBILE && 
      | DRM_TILCDC && 
      | FB_BACKLIGHT && 
      | FB_MX3 && 
      | USB_APPLEDISPLAY &&
      | FB_OLPC_DCON && 
      | ASUS_LAPTOP && 
      | SONY_LAPTOP && 
      | THINKPAD_ACPI && 
      | EEEPC_LAPTOP && 
      | ACPI_CMPC && 
      | SAMSUNG_Q10



