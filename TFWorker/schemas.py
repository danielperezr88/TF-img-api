schemas = {

    'InferHandler': {
        "type": "object",
        "properties": {
            "image": {
                "description": "Images to process",
                "type": "string"
            },
            "model": {
                "description": "Model to apply",
                "type": "string"
            }
        },
        "required": ["image"]
    }

}
