Rivellino 
=========

Rivellino is an ETL (Extract, Transform, Load) tool. It reads data from multiple data sources, transforms them into a format suitable for your data warehouse then loads them into the data warehouse tables.

Ruleset
--------

Rules are applied by ETL, and they are the logic behind the Transform part. The rules can be found in the `./ruleset` folder as YAML files. You can also create your own rules. 

There are two types of rules, `single` and `group` rules. A group rule is just a collection of multiple single rules so that you can run them all using a single command and control the order in which they are executed.

A single rule file contains the following fields:

* rule_description: Description for this rule and what is does.
* active: [yes|no] A non active rule is not run be default unless you run it by name or include it into a group rule.
* source_node: Name of the database, API or other sources of data. Nodes are defined in the `config.yml` file.
* destination_node: Name of the database, API or other destination of data. Nodes are defined in the `config.yml` file. This is normally the Datawarehouse de-normalized database your data end up in.
* destination_table: Name of the table into your destination database. This is normally the Datawarehouse de-normalized table your data end up in.
* action: The is what the ingress plugin processes. This can be a SQL statement or any other rules understood by the plugin so it knows what data to extract and how to present it to the egress plugin.
* ingress_plugin: Plugins will be discussed in the next section
* egress_plugin: Plugins will be discussed in the next section
* data_processors: Plugins will be discussed in the next section
* rule_type: single

A group rule file contains the following fields:

* rule_description: Description for this rule and what is does.
* active: [yes|no] A non active rule is not run be default unless you run it by name.
* members: A list of member rules, for now, you can only have single rules as members of a group rule, so we don't have recursion issues.
* rule_type: group

Currently rule actions can be either SQL strings, or in YAML format. It is the rule creators' responsibility to make sure the (ingress) plugin in each rule will comprehend the action field. 

In a YAML action, you can specify sub-rules inside any fields, so that the output of those rules populate such fields. For example, the following action:

    action: 
      sweets: 
        - cookies
        - chocolates
        - biscuits
      fruits: $rule:get_some_fruits.yml:fruit_names

Will be converted into the following, given that the ingress rule in `get_some_fruits.yml` produces a data of type `PluginsData` with some fruit names into the field `fruit_names`.

    action: 
      sweets: 
        - cookies
        - chocolates
        - biscuits
      fruits: 
        - apples
        - oranges
        - grapes

Plugins
--------

There are plugins to read and write data to data nodes (data sources and destinations). Ingress plugins read data from data sources, using the `action` field in the rule to decide how to read and transform this data. Egress rules on the other hand are responsible for writing the data in the data destination. 

In addition to Ingress and Egress plugins, users can also set Data Processors to alter the data on its way from Ingress plugin to the Egress one. Data Processors are nothing more but a list of plugins you set in your rule, and they are applyed in order.   

Plugns are located in `./plugins`. You too can write your own plugins. The most important aspect of a plugin is to be compliant with a rule. For example, a MySQL plugin knows that the `action` filed in a rule is a SQL statement and it excutes that statement. For a web API plugin for example, you have to agree on your own grammar for the rule's action so it knows how to deal with it. 

Some existing plugins include `dummy_plugin` which does absolutely nothing. You can use it in cases where you want your rule to only have one side, ingress or egress. The `screen_dump_plugin` is used for debugging purpose, when it is used as an egress plugin, it will just dump the data read by the ingress plugin.

__Note:__ I am planning to explain the plugins included and their rules syntax in a details later on.

Installation
-------------

You first need to install all required libraries:

    pip install -r requirements.txt

Then copy config.yml.example to config.yml

CLI
----

The ETL command is as follows:

    python rivellino.py [-h] [--list] [--run [RULE_NAME]]

To list existing rules:

    python rivellino.py --list

To run all active rules:

    python rivellino.py --run

To run a specific rules:

    python rivellino.py --run rule_name.yml

Example:
    
    py rivellino.py -p -r reset_datawarehouse.yml
    py rivellino.py -p -r populate_datawarehouse.yml


Why Rivellino
-------------

![Rivellino](docs/rivellino-icon.png)

Roberto Rivellino is a former Brazilian professional footballer. He was one of the stars of Brazil's 1970 FIFA World Cup winning team. His skills with the ball, are what this tools aspires to have with data.

Contacts
--------
 
+ Name: [Tarek Amr](http://tarekamr.appspot.com/)
+ Twitter: [@gr33ndata](https://twitter.com/gr33ndata)
