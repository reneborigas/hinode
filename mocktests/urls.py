from django.conf.urls import url

from mocktests import views


urlpatterns = [ 
    url(r'^$', views.list_mocktests, name='list_mocktests'),
    url(r'^create$', views.create_mocktest, name='create_mocktest'),
    url(r'^(?P<mocktest_id>\d+)$', views.edit_mocktest, name='edit_mocktest'),
    url(r'^(?P<mocktest_id>\d+)/results$', views.view_mocktest_results,
        name='view_mocktest_results'),
    url(r'^(?P<mocktest_id>\d+)/result/(?P<student_id>\d+)$',
        views.view_participant_result, name='view_participant_result'),
    url(r'^(?P<mocktest_id>\d+)/questions$', views.view_assigned,
    	name='view_assigned'),
    url(r'^(?P<mocktest_id>\d+)/sections$', views.view_sections,
    	name='view_sections'),    
    url(r'^(?P<mocktest_id>\d+)/sections/(?P<mocktestsection_id>\d+)$', views.edit_section, name='edit_section'),
    url(r'^(?P<mocktest_id>\d+)/create$', views.create_section, name='create_section'),
    url(r'^(?P<mocktest_id>\d+)/sections/(?P<mocktestsection_id>\d+)/subsections$', views.view_subsections,
    	name='view_subsections'),  
    url(r'^(?P<mocktest_id>\d+)/sections/(?P<mocktestsection_id>\d+)/subsections/(?P<mocktestsubsection_id>\d+)/sentences$', views.view_mocktest_sentences,
    	name='view_mocktest_sentences'),  
    url(r'^(?P<mocktest_id>\d+)/sections/(?P<mocktestsection_id>\d+)/subsections/(?P<mocktestsubsection_id>\d+)/sentences/(?P<mocktestsentence_id>\d+)$', views.edit_mocktest_sentence,
    	name='edit_mocktest_sentence'),  
    url(r'^(?P<mocktest_id>\d+)/sections/(?P<mocktestsection_id>\d+)/subsections/(?P<mocktestsubsection_id>\d+)/create$', views.create_mocktest_sentence, name='create_mocktest_sentence'),
    url(r'^(?P<mocktest_id>\d+)/sections/(?P<mocktestsection_id>\d+)/create$', views.create_subsection, name='create_subsection'),
    url(r'^(?P<mocktest_id>\d+)/sections/(?P<mocktestsection_id>\d+)/subsections/(?P<mocktestsubsection_id>\d+)$', views.edit_subsection, name='edit_subsection'),
    url(r'^(?P<mocktest_id>\d+)/s$', views.view_mocktest, name='view_mocktest'),
    url(r'^(?P<mocktest_id>\d+)/s/(?P<mocktestsection_id>\d+)$', views.view_mocktestsection, name='view_mocktestsection'),
    # url(r'^(?P<mocktest_id>\d+)/s/(?P<mocktestsection_id>\d+)/s/(?P<mocktestsubsection_id>\d+)$', views.view_mocktestsubsection, name='view_mocktestsubsection'),
    url(r'^(?P<mocktest_id>\d+)/s/(?P<mocktestsection_id>\d+)/p$', views.input_password, name='input_password'),
    url(r'^(?P<mocktest_id>\d+)/t$', views.take_mocktest, name='take_mocktest'),
    url(r'^(?P<mocktest_id>\d+)/result/s$', views.view_result,
    	name='view_result'),
]