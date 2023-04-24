..
    https://github.com/sphinx-doc/sphinx/issues/7912

{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :inherited-members:

   {% block methods %}

   .. rubric:: {{ _('Inheritance Diagram') }}

   .. inheritance-diagram:: {{ objname }}
      :parts: 1

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Variables & Properties') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block details %}

   .. rubric:: {{ _('Details') }}

   .. automethod:: __init__

   {% endblock %}
