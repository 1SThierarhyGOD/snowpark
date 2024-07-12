@@ -1,4 +1,4 @@
""" Hyper Extractor CLI utility	"""Hyper Extractor CLI utility.
Tableau Community supported Hyper API sample	Tableau Community supported Hyper API sample
@@ -47,10 +47,12 @@




class IllegalArgumentError(ValueError):	class IllegalArgumentError(ValueError):
    """Exception: Command line args fail validation."""

    pass	    pass




def exclusive_args(args, *arg_names, required=True, message=None):	def _exclusive_args(args, *arg_names, required=True, message=None):
    count_args = 0	    count_args = 0
    for arg_name in arg_names:	    for arg_name in arg_names:
        if bool(vars(args).get(arg_name)):	        if bool(vars(args).get(arg_name)):
@@ -69,15 +71,15 @@ def exclusive_args(args, *arg_names, required=True, message=None):
                raise IllegalArgumentError(message)	                raise IllegalArgumentError(message)




def required_arg(args, arg_name, message=None):	def _required_arg(args, arg_name, message=None):
    if not bool(vars(args).get(arg_name)):	    if not bool(vars(args).get(arg_name)):
        if message is None:	        if message is None:
            raise IllegalArgumentError("Missing required argument:{}".format(arg_name))	            raise IllegalArgumentError("Missing required argument:{}".format(arg_name))
        else:	        else:
            raise IllegalArgumentError(message)	            raise IllegalArgumentError(message)




def add_arg_with_default(parser, config, default_config_key, help, required, *args, **kwargs):	def _add_arg_with_default(parser, config, default_config_key, help, required, *args, **kwargs):
    default_value = None	    default_value = None
    if default_config_key is not None:	    if default_config_key is not None:
        # May have to walk the tree in YAML file	        # May have to walk the tree in YAML file
@@ -106,7 +108,7 @@ def add_arg_with_default(parser, config, default_config_key, help, required, *ar
        parser.add_argument(*args, default=default_value, help=help, **kwargs)	        parser.add_argument(*args, default=default_value, help=help, **kwargs)




def get_int_from_arg(this_str, arg_name, is_required=False):	def _get_int_from_arg(this_str, arg_name, is_required=False):
    if this_str is None:	    if this_str is None:
        if is_required:	        if is_required:
            raise IllegalArgumentError("Missing required argument:{}".format(arg_name))	            raise IllegalArgumentError("Missing required argument:{}".format(arg_name))
@@ -121,6 +123,7 @@ def get_int_from_arg(this_str, arg_name, is_required=False):




def main():	def main():
    """Command line utility for clouddb_extractor."""
    # Load defaults	    # Load defaults
    config = yaml.safe_load(open("config.yml"))	    config = yaml.safe_load(open("config.yml"))


@@ -147,7 +150,7 @@ def main():
        choices=["load_sample", "export_load", "append", "update", "delete"],	        choices=["load_sample", "export_load", "append", "update", "delete"],
        help="Select the function to call",	        help="Select the function to call",
    )	    )
    add_arg_with_default(	    _add_arg_with_default(
        parser,	        parser,
        config,	        config,
        "default_extractor",	        "default_extractor",
@@ -160,7 +163,7 @@ def main():
        "--source_table_id",	        "--source_table_id",
        help="Fully qualified table identifier from source database",	        help="Fully qualified table identifier from source database",
    )	    )
    add_arg_with_default(parser, config, "sample_rows", "Defines the number of rows to use with LIMIT when command=load_sample", False, "--sample_rows")	    _add_arg_with_default(parser, config, "sample_rows", "Defines the number of rows to use with LIMIT when command=load_sample", False, "--sample_rows")


    parser.add_argument(	    parser.add_argument(
        "--sql",	        "--sql",
@@ -184,13 +187,13 @@ def main():
    )	    )


    # Tableau Server / Tableau Online options	    # Tableau Server / Tableau Online options
    add_arg_with_default(parser, config, "tableau_env.server_address", "Tableau connection string", True, "--tableau_hostname", "-H")	    _add_arg_with_default(parser, config, "tableau_env.server_address", "Tableau connection string", True, "--tableau_hostname", "-H")
    add_arg_with_default(parser, config, "tableau_env.site_id", "Tableau site id", True, "--tableau_site_id", "-S")	    _add_arg_with_default(parser, config, "tableau_env.site_id", "Tableau site id", True, "--tableau_site_id", "-S")
    add_arg_with_default(parser, config, "tableau_env.project", "Target project name", True, "--tableau_project", "-P")	    _add_arg_with_default(parser, config, "tableau_env.project", "Target project name", True, "--tableau_project", "-P")
    add_arg_with_default(parser, config, "tableau_env.datasource", "Target datasource name", True, "--tableau_datasource")	    _add_arg_with_default(parser, config, "tableau_env.datasource", "Target datasource name", True, "--tableau_datasource")
    add_arg_with_default(parser, config, "tableau_env.username", "Tableau user name", False, "--tableau_username", "-U")	    _add_arg_with_default(parser, config, "tableau_env.username", "Tableau user name", False, "--tableau_username", "-U")
    add_arg_with_default(parser, config, "tableau_env.token_name", "Personal access token name", False, "--tableau_token_name")	    _add_arg_with_default(parser, config, "tableau_env.token_name", "Personal access token name", False, "--tableau_token_name")
    add_arg_with_default(parser, config, "tableau_env.token_secretfile", "File containing personal access token secret", False, "--tableau_token_secretfile")	    _add_arg_with_default(parser, config, "tableau_env.token_secretfile", "File containing personal access token secret", False, "--tableau_token_secretfile")


    # Parse Args	    # Parse Args
    args = parser.parse_args()	    args = parser.parse_args()
@@ -199,14 +202,14 @@ def main():
    db_env = config.get(selected_extractor)	    db_env = config.get(selected_extractor)


    # Check for conflicting args	    # Check for conflicting args
    exclusive_args(	    _exclusive_args(
        args,	        args,
        "tableau_token_name",	        "tableau_token_name",
        "tableau_username",	        "tableau_username",
        required=True,	        required=True,
        message="Specify either tableau_token_name OR tableau_username",	        message="Specify either tableau_token_name OR tableau_username",
    )	    )
    exclusive_args(	    _exclusive_args(
        args,	        args,
        "sql",	        "sql",
        "sqlfile",	        "sqlfile",
@@ -233,7 +236,7 @@ def main():


    # Tableau Authentication can be by token or username/password (prompt)	    # Tableau Authentication can be by token or username/password (prompt)
    if args.tableau_token_name:	    if args.tableau_token_name:
        required_arg(	        _required_arg(
            args,	            args,
            "tableau_token_secretfile",	            "tableau_token_secretfile",
            "Must specify tableau_token_secretfile with tableau_token_name",	            "Must specify tableau_token_secretfile with tableau_token_name",
@@ -262,7 +265,7 @@ def main():
        )	        )


    if selected_command == "load_sample":	    if selected_command == "load_sample":
        required_arg(	        _required_arg(
            args,	            args,
            "sample_rows",	            "sample_rows",
            "Must specify sample_rows when action is load_sample",	            "Must specify sample_rows when action is load_sample",
@@ -271,7 +274,7 @@ def main():
            sql_query=sql_string,	            sql_query=sql_string,
            source_table=args.source_table_id,	            source_table=args.source_table_id,
            tab_ds_name=args.tableau_datasource,	            tab_ds_name=args.tableau_datasource,
            sample_rows=get_int_from_arg(args.sample_rows, "sample_rows", True),	            sample_rows=_get_int_from_arg(args.sample_rows, "sample_rows", True),
        )	        )


    if selected_command == "export_load":	    if selected_command == "export_load":
@@ -289,7 +292,7 @@ def main():
        )	        )


    if selected_command in ("update", "delete"):	    if selected_command in ("update", "delete"):
        exclusive_args(	        _exclusive_args(
            args,	            args,
            "match_columns",	            "match_columns",
            "match_conditions_json",	            "match_conditions_json",