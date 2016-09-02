#!/bin/bash

. /usr/share/preupgrade/common.sh

#END GENERATED SECTION

# This check can be used if you need root privilegues
check_root

# Copy your config file from original to target system 
# to Temporary Directory
CONFIG_FILE="full_path_to_your_config_file"
mkdir -p $VALUE_TMP_PREUPGRADE/cleanconf/$(dirname $CONFIG_FILE)
cp $CONFIG_FILE $VALUE_TMP_PREUPGRADE/cleanconf/$CONFIG_FILE

# Now check you configuration file for options
# and for other stuff related with configuration

# If configuration can be used on target system
# the exit should be RESULT_PASS

# If configuration can not be used on target system
# scenario then result should be RESULT_FAIL. And script has to show log_slight_risk or log_medium_risk.
# Correction of configuration file is provided either by solution script
# or by postupgrade script located in $VALUE_TMP_PREUPGRADE/postupgrade.d/

# if configuration file can be fixed then fix them in directory
# $VALUE_TMP_PREUPGRADE/cleanconf/$CONFIG_FILE and result should be RESULT_FIXED
# More information about this issues should be described in solution.txt file
# as reference to KnowledgeBase article.

grep "Sometext" $CONFIG_FILE
if [ $? -ne 0 ]; then
    log_error "Config file $CONFIG_FILE can not be used on target system"
    log_slight_risk "We assessed this field and have not found any issues. See man preupgrade-assistant-api for more details"
    log_medium_risk "iIt is likely that the area causes a problem in case of the inplace upgrade. See man preupgrade-assistant-api for more details"
    exit_fail
fi

exit_pass
