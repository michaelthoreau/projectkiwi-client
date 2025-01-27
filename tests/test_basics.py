import pytest
import os
import numpy as np
import projectkiwi3
import projectkiwi3.models



def getClient():
    """Return a client with the API key and URL from the environment
    """
    key = os.environ.get("PROJECTKIWI3_API_KEY")
    url = os.environ.get("PROJECTKIWI3_URL")

    assert key, "PROJECTKIWI3_API_KEY must be set in the environment"
    assert url, "PROJECTKIWI3_URL must be set in the environment"
    return projectkiwi3.Client(key, url)

def test_create_project():
    """Create a project and check everything looks good to me
    """

    client = getClient()
    PROJ_NAME = "test"

    project = client.createProject(PROJ_NAME)

    assert project.id is not None
    assert project.name == PROJ_NAME
    assert project.createdAt
    assert project.modifiedAt
    assert project.owner





def test_add_label_and_annotation():
    """Create a project and add an annotation
    """

    client = getClient()
    PROJ_NAME = "test"

    project = client.createProject(PROJ_NAME)

    LABEL_NAME = "test_label"
    LABEL_COLOR = "rgb(0, 69, 42)"

    label = client.addLabel(project.id, name=LABEL_NAME, color=LABEL_COLOR)

    assert label.name == LABEL_NAME
    assert label.color == LABEL_COLOR

    # CHAAAD
    ANNOTATION_COORDS = [
        [
            16.268203655953613,
            23.383943456026273
        ],
        [
            14.935034924543771,
            23.108145130196803
        ],
        [
            15.76079746570636,
            16.90123576626638
        ],
        [
            13.399196837322421,
            14.817993358986172
        ],
        [
            14.211783577458817,
            9.775538609780241
        ],
        [
            15.783947274898964,
            7.296930569584262
        ],
        [
            22.459154641909862,
            10.472609517588566
        ],
        [
            24.034652422437063,
            15.63906863793278
        ],
        [
            23.922648463490617,
            19.680835605784765
        ],
        [
            16.268203655953613,
            23.383943456026273
        ]
    ]
 

    ANNO_TYPE = "Polygon"
    ANNO_CONF = 0.69

    annotation = client.addAnnotation(project.id,
                                      coordinates=ANNOTATION_COORDS,
                                      shape=ANNO_TYPE,
                                      labelId=label.id,
                                      confidence=ANNO_CONF)

    assert annotation.label.id == label.id
    assert annotation.id
    assert annotation.confidence == ANNO_CONF
    assert annotation.createdAt
    assert annotation.modifiedAt
    assert annotation.shape == ANNO_TYPE
    assert np.isclose(annotation.coordinates, ANNOTATION_COORDS).all()



def test_add_multiple_annotations():
    """Create a project and add an annotation
    """

    client = getClient()
    PROJ_NAME = "test"

    project = client.createProject(PROJ_NAME)



    label1 = client.addLabel(project.id, name="chad", color="rgb(0, 69, 42)")
    label2 = client.addLabel(project.id, name="maverick", color="rgb(0, 69, 42)")


    # CHAAAD
    ANNO1_TYPE = "Polygon"
    ANNO1_CONF = 0.69
    ANNO1_COORDS = [
        [
            16.268203655953613,
            23.383943456026273
        ],
        [
            14.935034924543771,
            23.108145130196803
        ],
        [
            15.76079746570636,
            16.90123576626638
        ],
        [
            13.399196837322421,
            14.817993358986172
        ],
        [
            14.211783577458817,
            9.775538609780241
        ],
        [
            15.783947274898964,
            7.296930569584262
        ],
        [
            22.459154641909862,
            10.472609517588566
        ],
        [
            24.034652422437063,
            15.63906863793278
        ],
        [
            23.922648463490617,
            19.680835605784765
        ],
        [
            16.268203655953613,
            23.383943456026273
        ]
    ]
 

    ANNO2_TYPE = "Point"
    ANNO2_CONF = 0.42
    # Maverick
    ANNO2_COORDS = [[-100.19435596377956, 31.836754697531916]]
   

    annotations = [
        projectkiwi3.models.AnnotationPayload(
            coordinates = ANNO1_COORDS,
            shape = ANNO1_TYPE,
            labelId = label1.id,
            confidence= ANNO1_CONF
            ),
        projectkiwi3.models.AnnotationPayload(
            coordinates = ANNO2_COORDS,
            shape = ANNO2_TYPE,
            labelId = label2.id,
            confidence= ANNO2_CONF
            )
    ]

    annotations = client.addAnnotations(project.id, annotations)

    assert annotations[0].label.id == label1.id
    assert annotations[0].id
    assert annotations[0].confidence == ANNO1_CONF
    assert annotations[0].createdAt
    assert annotations[0].modifiedAt
    assert annotations[0].shape == ANNO1_TYPE
    assert np.isclose(annotations[0].coordinates, ANNO1_COORDS).all()

    assert annotations[1].label.id == label2.id
    assert annotations[1].id
    assert annotations[1].confidence == ANNO2_CONF
    assert annotations[1].createdAt
    assert annotations[1].modifiedAt
    assert annotations[1].shape == ANNO2_TYPE
    assert np.isclose(annotations[1].coordinates, ANNO2_COORDS).all()
