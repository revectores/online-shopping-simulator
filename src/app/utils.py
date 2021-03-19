from playhouse.shortcuts import dict_to_model, model_to_dict

def models_to_dict(models):
    return {model.id: model_to_dict(model) for model in models}

def models_to_list(models):
	return [model_to_dict(model) for model in models]
