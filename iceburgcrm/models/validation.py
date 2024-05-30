import re, datetime, sys
# import json

class Validation():

    def __init__(self):
        self.error_message_templates = self.get_error_message_templates()
        self.custom_error_messages = {}
        self.errors = []


    def validate(self, data, rules, custom_messages=None):
        """Validate the 'data' according to the 'rules' given, returns a list of errors named 'errors'"""

        if custom_messages:
            self.custom_error_messages = custom_messages
        
        for field_name in rules:

            field_rules = rules[field_name].split('|')
            
            field_errors = []

            for rule in field_rules:
                field_errors.extend(self.validate_field_rule(data, field_name, rule, field_rules))

            self.errors.extend(field_errors)

        return self.errors

    def validate_field_rule(self, data, field_name, rule, field_rules=None):
        """Validates the data of the field based on the rule assigned"""

        rule_error = ""

        if rule.startswith("after"):
            rule_error = self.validate_after_date_fields(data,field_name,field_rules,rule)

        elif rule == "alpha":
            rule_error = self.validate_alpha_fields(data,field_name)

        elif rule == "alpha_num":
            rule_error = self.validate_alpha_num_fields(data,field_name)

        elif rule.startswith("before"):
            rule_error = self.validate_before_date_fields(data,field_name,field_rules,rule)

        elif rule.startswith("between"):
            rule_error = self.validate_between_fields(data, field_name, rule)

        elif rule == "boolean":
            rule_error = self.validate_boolean_fields(data,field_name)

        elif rule.startswith("confirmed"):
            rule_error = self.validate_confirmed_fields(data,field_name)

        elif rule == "date":
            rule_error = self.validate_date_fields(data,field_name,field_rules)

        elif rule == "digits":
            rule_error = self.validate_integer_fields(data,field_name)

        elif rule.startswith("different"):
            rule_error = self.validate_different_fields(data,field_name, rule)

        elif rule == "email":
            rule_error = self.validate_email_fields(data,field_name)

        elif rule.startswith("in"):
            rule_error = self.validate_in_fields(data,field_name, rule)

        elif rule == "ip":
            rule_error = self.validate_ip_fields(data,field_name)

        elif rule.startswith("max"):
            rule_error = self.validate_max_fields(data,field_name,rule)

        elif rule.startswith("min"):
            rule_error = self.validate_min_fields(data,field_name,rule)

        elif rule.startswith("not_in"):
            rule_error = self.validate_not_in_fields(data,field_name,rule)

        elif rule == "present":
            rule_error = self.validate_present_fields(data,field_name)

        elif rule == "phone":
            rule_error = self.validate_phone_fields(data, field_name)

        elif rule.startswith("regex"):
            rule_error = self.validate_regex_fields(data,field_name, rule)

        elif rule == "required":
            rule_error = self.validate_required_fields(data, field_name)

        elif rule.startswith("same"):
            rule_error = self.validate_same_fields(data, field_name, rule)

        elif rule.startswith("size"):
            rule_error = self.validate_size_fields(data,field_name,rule)

        elif rule == "website":
            rule_error = self.validate_website_fields(data,field_name)

        return rule_error

    def validate_required_fields(self, data, field_name):
        """Used for validating required fields, returns a list of error messages"""

        errs = []
        try:
            if data[field_name] == '':
                errs.append(self.return_field_message(field_name,"required"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'required'))

        return errs        

    def validate_date_fields(self, data, field_name, field_rules):
        """Used for validating date fields, returns a list of error messages"""

        errs = []
        date_format = self.retrieve_date_format(field_rules)
        try:
            datetime.datetime.strptime(data[field_name], date_format)
        except ValueError:
            errs.append(self.return_field_message(field_name,"date"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'date'))
            
        return errs

    def validate_before_date_fields(self, data, field_name, field_rules,rule):
        """Used for validating fields for a date before the specified date value, returns a list of error messages"""

        #retrieve the value for that before rule
        before_date_value = rule.split(':')[1]

        errs = []
        date_format = self.retrieve_date_format(field_rules)

        try:
            date_entered = datetime.datetime.strptime(data[field_name], date_format).date()
            before_date = datetime.datetime.strptime(before_date_value, date_format).date()
            
            if date_entered >= before_date:
                errs.append(self.return_field_message(field_name,"before"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'before'))
        except ValueError:
            #because the value will not be a valid date according to the format
            errs.append(self.return_field_message(field_name,"date"))

        return errs

    def validate_after_date_fields(self, data, field_name, field_rules,rule):
        """Used for validating fields for a date after the specified date value, returns a list of error messages"""

        #retrieve the value for that after rule
        after_date_value = rule.split(':')[1]

        errs = []
        date_format = self.retrieve_date_format(field_rules)

        try:
            date_entered = datetime.datetime.strptime(data[field_name], date_format).date()
            after_date = datetime.datetime.strptime(after_date_value, date_format).date()

            if date_entered <= after_date:
                errs.append(self.return_field_message(field_name,"after"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'after date'))
        except ValueError:
            #because the value will not be a valid date according to the format
             errs.append(self.return_field_message(field_name,"date"))

        return errs

    def validate_integer_fields(self, data, field_name):
        """Used for validating integer fields, returns a list of error messages"""

        errs = []
        try:
            if not data[field_name].isdigit():
                errs.append(self.return_field_message(field_name,"integer"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'integer'))
        return errs

    def validate_email_fields(self, data, field_name):
        """Used for validating email fields, returns a list of error messages"""

        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        errs,result = self.match_regular_expression(regex,data[field_name],"email")

        #in case the RE did not match or there was a key error
        if not result:
            errs.append(self.return_field_message(field_name,"email"))
        return errs

    def validate_regex_fields(self, data, field_name, rule):
        """Used for validating field data to match a regular expression, returns a list of error messages"""

        regex = str(rule.split(':')[1])
        errs,result = self.match_regular_expression(regex,data[field_name],"regex")

        #in case the RE did not match or there was a key error
        if not result:
            errs.append(self.return_field_message(field_name,"regex"))
        return errs

    def validate_present_fields(self, data, field_name):
        """Used for validating present fields, returns a list of error messages"""

        errs = []
        try:
            if not data.__contains__(field_name):
                errs.append(self.return_field_message(field_name,"present"))	
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'present'))
            
        return errs

    def validate_boolean_fields(self, data, field_name):
        """Used for validating boolean fields, returns a list of error messages"""

        errs = []
        bool_values = [1,0,"1","0","false","true",False,True]

        try:
            if data[field_name] not in bool_values:
                errs.append(self.return_field_message(field_name,"boolean"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'boolean'))
        return errs

    def validate_ip_fields(self, data, field_name):
        """Used for validating fields having IP Address, returns a list of error messages"""

        regex = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        errs,result = self.match_regular_expression(regex,data[field_name],"ip")

        #in case the RE did not match or there was a key error
        if not result:
            errs.append(self.return_field_message(field_name,"ip"))
        return errs

    def validate_phone_fields(self, data, field_name):
        """Used for validating fields having phone numbers, returns a list of error messages"""

        regex = r'^(?:\+?93)?[07]\d{9,13}$'
        errs,result = self.match_regular_expression(regex,data[field_name],"phone")

        #in case the RE did not match or there was a key error
        if not result:
            errs.append(self.return_field_message(field_name,"phone"))
            
        return errs

    def validate_website_fields(self, data, field_name):
        """Used for validating fields having website addresses, returns a list of error messages"""

        regex = r'(http(s)?://)?([\w-]+\.)+[\w-]+[\w-]+[\.]+[\.com]+([./?%&=]*)?'
        errs,result = self.match_regular_expression(regex,data[field_name],"website")

        #in case the RE did not match or there was a key error
        if not result:
            errs.append(self.return_field_message(field_name,"website"))

        return errs

    def validate_alpha_fields(self, data, field_name):
        """Used for validating fields for alphabets only, returns a list of error messages"""

        errs = []
        try:
            if not data[field_name].isalpha():
                errs.append(self.return_field_message(field_name,"alpha"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'alpha'))
        
        return errs

    def validate_alpha_num_fields (self, data, field_name):
        """Used for validating fields for alphabets and numbers, returns a list of error messages"""

        errs = []
        try:
            if not data[field_name].isalnum():
                errs.append(self.return_field_message(field_name,"alpha_num"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'alpha numeric'))

        return errs

    
    def validate_max_fields(self, data, field_name, rule):
        """Adjust to handle string length or numeric maximum based on context"""
        max_value = int(rule.split(':')[1])
        errs = []
        field_value = data.get(field_name, "")

        # Check if field value exceeds max_value
        if isinstance(field_value, str) and len(field_value) > max_value:
            errs.append(f"{field_name} exceeds maximum length of {max_value}.")
        elif isinstance(field_value, (int, float)) and field_value > max_value:
            errs.append(f"{field_name} exceeds maximum value of {max_value}.")

        return errs

    def validate_min_fields(self, data, field_name, rule):
        """Used for validating fields for a minimum integer value, returns a list of error messages"""

        #retrieve the value for that min rule
        min_value = int(rule.split(':')[1])

        errs = []
        try:
            if data[field_name].isdigit():
                if int(data[field_name]) < min_value:
                    errs.append(self.return_field_message(field_name,"min"))
            else:
                if len(data[field_name]) < min_value:
                    errs.append(self.return_field_message(field_name,"min"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'minimum'))

        return errs

    def validate_confirmed_fields(self, data, field_name):
        """if the field under validation is a password, a matching password_confirmation field must be present in the data, 
            returns a list of error messages"""

        errs = []
        confirmation_field = field_name + "_confirmation"

        try:
            if confirmation_field not in data.keys():
                errs.append(self.return_field_message(field_name,"confirmed"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'confirmed'))
        return errs

    def validate_size_fields(self, data, field_name, rule):
        """Used for validating fields for a maximum number of characters in a string value, returns a list of error messages"""

        errs = []
        try:
            #retrieve the value for that size rule
            size_value = int(rule.split(':')[1])

            if len(data[field_name]) >= size_value:
                errs.append(self.return_field_message(field_name,"size"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'size'))
        except ValueError:
            errs.append(self.return_field_message(field_name,"size"))
            
        return errs

    def validate_not_in_fields(self, data, field_name, rule):
        """Used for validating fields for some number of values to avoid, returns a list of error messages"""

        #retrieve the value for that not_in rule
        ls = rule.split(':')[1].split(',')
        errs = []

        try:
            if data[field_name] in ls:
                errs.append(self.return_field_message(field_name,'not_in'))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'not_in'))

        return errs

    def validate_in_fields(self, data, field_name, rule):
        """Used for validating fields for some number of values to allow, returns a list of error messages"""

        #retrieve the value for that in rule
        ls = rule.split(':')[1].split(',')
        errs = []

        try:
            if data[field_name] not in ls:
                errs.append(self.return_field_message(field_name, "in"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'in'))
        return errs


    def validate_different_fields(self, data, field_name, rule):
        """
        Used for validating fields whose value should be different than the value of some other field, 
        returns a list of error messages
        """

        #retrieve the value for the different rule
        ls = rule.split(':')[1].split(',')[0]
        errs = []

        try:
            if data[field_name] == data[ls]:
                errs.append(self.return_field_message(field_name,"different"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'different'))
        except Exception:
                errs.append("Error Occured",sys.exc_info())
         
        return errs

    def validate_same_fields(self, data, field_name, rule):
        """
        Used for validating fields whose value should be the same as some other field value, 
        returns a list of error messages
        """

        #retrieve the value for the same rule
        ls = rule.split(':')[1].split(',')
        errs = []

        try:
            if data[field_name] != data[ls[0]]:
                errs.append(self.return_field_message(field_name, "same"))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,'same'))
        return errs


    def validate_between_fields(self, data, field_name, rule):
        """Used for validating fields for a number between two digits to allow, returns a list of error messages"""

        #retrieve the value for the between rule
        ls = rule.split(':')[1].split(',')
        errs = []

        try:
            if int(data[field_name]) < int(ls[0]) or int(data[field_name]) > int(ls[1]):
                errs.append(self.return_field_message(field_name,'between'))
        except KeyError:
            errs.append(self.return_no_field_message(field_name,"between"))
        except ValueError:
            errs.append(field_name + " can not be empty")
        return errs

    def retrieve_date_format(self,field_rules):
        #loop through each rule for the particular field to check if there is any date_format rule assigned
        for rule in field_rules:
            #if there is a date_format rule assigned then fetch the date format from that
            if rule.startswith("date_format"):
                date_format = rule.split(":")[1]
                
                return date_format

        #if no date_format found, return the default date format
        return '%m/%d/%Y'

    def match_regular_expression(self,regex,field_value,rule_name):
        comp_re = re.compile(regex, re.IGNORECASE)
        errs = []

        try:
            result = comp_re.match(field_value)
        except KeyError:
            errs.append(self.return_no_field_message(field_value,rule_name))
            result = "error"

        return errs,result

    # def load_json_file(self,file_name):
    #     with open(file_name) as f:
    #         t = f.read()
    #         return json.loads(t)

    def return_no_field_message(self, field_name, rule_name):
        if self.custom_error_messages.__contains__(field_name+".no_field"):
            return self.custom_error_messages[field_name+".no_field"]
        else:
            return self.error_message_templates['no_field'] % (field_name,rule_name)

    def return_field_message(self, field_name, rule_name):
        if self.custom_error_messages.__contains__(field_name+"."+rule_name):
            return self.custom_error_messages[field_name+"."+rule_name]
        else:
            return self.error_message_templates[rule_name] % (field_name)

    def is_valid(self, data, rules):
        """Validates the data according to the rules, returns True if the data is valid, and False if the data is invalid"""

        errors = self.validate(data,rules)

        self.errors = errors

        return not len(errors) > 0

    def get_error_message_templates(self):
        return {
            "after": "'%s' is an invalid after date",
            "alpha":"'%s' can have only alphabets",
            "alpha_num":"'%s' can have only alphabets or numbers",        
            "before":"'%s' is an invalid before date ",
            "between":"'%s' has an invalid value for between field",
            "boolean":"'%s' has invalid value for boolean field",
            "confirmed":"'%s' must have a pair field",
            "date":"'%s' value does not match date format",
            "digits":"'%s' must be an integer",
            "different":"'%s' has invalid value for same rule ",
            "email":"'%s' must be a valid email address",
            "in":"'%s' has invalid value for in rule",
            "ip":"'%s' must be a valid IP address",
            "max":"The maximum value for the field '%s' is invalid",
            "min":"The minimum value for the field '%s' is invalid",
            "not_in":"'%s' has invalid value for not_in rule",
            "present":"The data dictionary must have a nullable field name '%s'",
            "phone":"'%s' must be a valid Phone Number",
            "regex":"'%s' field does not match the RE ",
            "required":"'%s' must be filled",
            "same":"'%s' has invalid value for same rule",
            "size":"'%s' has invalid value for size rule",
            "website":"'%s' must be a valid Website URL",
            "no_field":"No field named '%s' to validate for %s rule"
        }
    
    def get_custom_error_messages(self):
        return {
            "_comment": "You did not provide any field named <feld_name> in your data dictionary",
            "field_name.rule":"You did not provide any field named field_name in your data dictionary",
            "month_day.regex":"You did not provide any field named month_day in your data dictionary",
            "phone.max":"You did not provide any field named phone in your data dictionary",
            "month_day.required":"You did not provide any field named month_day in your data dictionary",
            "new_password_confirmation.same":"You did not provide any field named %s in your data dictionary",
            "phone.no_field":"You did not provide any field named phone in your data dictionary",
            "birthday.date_format":"You did not provide any field named birthday in your data dictionary",
            "new_password.alpha":"field new_password can only have alphabet values",
            "host.no_field":"You did not provide any field named host in your data dictionary",
            "email.no_field":"You did not provide any field named email in your data dictionary",
            "nationality.no_field":"You did not provide any field named nationality in your data dictionary",
            "active.no_field":"You did not provide any field named active in your data dictionary",
            "age.no_field":"You did not provide any field named age in your data dictionary"
        }