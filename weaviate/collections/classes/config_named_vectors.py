from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import AnyHttpUrl, Field
from weaviate.collections.classes.config_vectorizers import (
    _ConfigCreateModel,
    _Img2VecNeuralConfig,
    _Multi2VecBindConfig,
    _Multi2VecClipConfig,
    _Ref2VecCentroidConfig,
    _Text2VecAWSConfig,
    _Text2VecAzureOpenAIConfig,
    _Text2VecCohereConfig,
    _Text2VecContextionaryConfig,
    _Text2VecGPT4AllConfig,
    _Text2VecHuggingFaceConfig,
    _Text2VecJinaConfig,
    _Text2VecOpenAIConfig,
    _Text2VecPalmConfig,
    _Text2VecTransformersConfig,
    AWSModel,
    CohereModel,
    CohereTruncation,
    JinaModels,
    Multi2VecField,
    OpenAIModel,
    OpenAIType,
    Vectorizers,
    _map_multi2vec_fields,
)
from weaviate.collections.classes.config_vector_index import (
    _VectorIndexConfigCreate,
    VectorIndexType,
)


class _NamedVectorizerConfigCreate(_ConfigCreateModel):
    vectorizer: Vectorizers
    properties: Optional[List[str]] = Field(default=None, min_length=1, alias="source_properties")

    def _to_dict(self) -> Dict[str, Any]:
        return self._to_vectorizer_dict(self.vectorizer, super()._to_dict())

    @staticmethod
    def _to_vectorizer_dict(vectorizer: Vectorizers, values: Dict[str, Any]) -> Dict[str, Any]:
        return {str(vectorizer.value): values}


class _Text2VecOpenAIConfigNamed(_Text2VecOpenAIConfig, _NamedVectorizerConfigCreate):
    pass


class _Text2VecContextionaryConfigNamed(_Text2VecContextionaryConfig, _NamedVectorizerConfigCreate):
    pass


class _Text2VecCohereConfigNamed(_Text2VecCohereConfig, _NamedVectorizerConfigCreate):
    pass


class _Text2VecAWSConfigNamed(_Text2VecAWSConfig, _NamedVectorizerConfigCreate):
    pass


class _Img2VecNeuralConfigNamed(_Img2VecNeuralConfig, _NamedVectorizerConfigCreate):
    pass


class _Multi2VecClipNamed(_Multi2VecClipConfig, _NamedVectorizerConfigCreate):
    pass


class _Multi2VecBindNamed(_Multi2VecBindConfig, _NamedVectorizerConfigCreate):
    pass


class _Ref2VecCentroidConfigNamed(_Ref2VecCentroidConfig, _NamedVectorizerConfigCreate):
    pass


class _Text2VecAzureOpenAIConfigNamed(_Text2VecAzureOpenAIConfig, _NamedVectorizerConfigCreate):
    pass


class _Text2VecGPT4AllConfigNamed(_Text2VecGPT4AllConfig, _NamedVectorizerConfigCreate):
    pass


class _NoneConfigNamed(_NamedVectorizerConfigCreate):
    vectorizer: Vectorizers = Field(default=Vectorizers.NONE, frozen=True, exclude=True)


class _Text2VecHuggingFaceConfigNamed(_Text2VecHuggingFaceConfig, _NamedVectorizerConfigCreate):
    pass


class _Text2VecPalmConfigNamed(_Text2VecPalmConfig, _NamedVectorizerConfigCreate):
    pass


class _Text2VecTransformersConfigNamed(_Text2VecTransformersConfig, _NamedVectorizerConfigCreate):
    pass


class _Text2VecJinaConfigNamed(_Text2VecJinaConfig, _NamedVectorizerConfigCreate):
    pass


class _NamedVectorConfigCreate(_ConfigCreateModel):
    name: str
    vectorizer: _NamedVectorizerConfigCreate
    vectorIndexType: VectorIndexType = Field(default=VectorIndexType.HNSW, exclude=True)
    vectorIndexConfig: Optional[_VectorIndexConfigCreate] = Field(
        default=None, alias="vector_index_config"
    )

    def _to_dict(self) -> Dict[str, Any]:
        ret_dict: Dict[str, Any] = {"vectorizer": self.vectorizer._to_dict()}

        if self.vectorIndexConfig is not None:
            ret_dict["vectorIndexType"] = self.vectorIndexConfig.vector_index_type().value
            ret_dict["vectorIndexConfig"] = self.vectorIndexConfig._to_dict()
        else:
            ret_dict["vectorIndexType"] = self.vectorIndexType.value

        return ret_dict


class _NamedVectors:
    @staticmethod
    def none(
        name: str, vector_index_config: Optional[_VectorIndexConfigCreate] = None
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using no vectorizer. You will need to provide the vectors yourself.

        Arguments:
            `name`
                The name of the named vector.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_NoneConfigNamed(),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_cohere(
        name: str,
        source_properties: Optional[List[str]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
        base_url: Optional[AnyHttpUrl] = None,
        model: Optional[Union[CohereModel, str]] = None,
        truncate: Optional[CohereTruncation] = None,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec_cohere` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-cohere)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
            `model`
                The model to use. Defaults to `None`, which uses the server-defined default.
            `truncate`
                The truncation strategy to use. Defaults to `None`, which uses the server-defined default.
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
            `base_url`
                The base URL to use where API requests should go. Defaults to `None`, which uses the server-defined default.

        Raises:
            `pydantic.ValidationError` if `truncate` is not a valid value from the `CohereModel` type.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecCohereConfigNamed(
                source_properties=source_properties,
                baseURL=base_url,
                model=model,
                truncate=truncate,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_contextionary(
        name: str,
        source_properties: Optional[List[str]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec_contextionary` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-contextionary)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecContextionaryConfigNamed(
                source_properties=source_properties,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_openai(
        name: str,
        source_properties: Optional[List[str]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
        model: Optional[Union[OpenAIModel, str]] = None,
        model_version: Optional[str] = None,
        type_: Optional[OpenAIType] = None,
        base_url: Optional[AnyHttpUrl] = None,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec_openai` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-openai)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
            `model`
                The model to use. Defaults to `None`, which uses the server-defined default.
            `model_version`
                The model version to use. Defaults to `None`, which uses the server-defined default.
            `type_`
                The type of model to use. Defaults to `None`, which uses the server-defined default.
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
            `base_url`
                The base URL to use where API requests should go. Defaults to `None`, which uses the server-defined default.

        Raises:
            `pydantic.ValidationError` if `type_` is not a valid value from the `OpenAIType` type.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecOpenAIConfigNamed(
                source_properties=source_properties,
                baseURL=base_url,
                model=model,
                modelVersion=model_version,
                type_=type_,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_aws(
        name: str,
        model: Union[AWSModel, str],
        region: str,
        source_properties: Optional[List[str]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec_aws` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-aws)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `model`
                The model to use, REQUIRED.
            `region`
                The AWS region to run the model from, REQUIRED.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecAWSConfigNamed(
                source_properties=source_properties,
                model=model,
                region=region,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def img2vec_neural(
        name: str,
        image_fields: List[str],
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
    ) -> _NamedVectorConfigCreate:
        """Create a `Img2VecNeuralConfig` object for use when vectorizing using the `img2vec-neural` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/img2vec-neural)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `image_fields`
                The image fields to use. This is a required field and must match the property fields
                of the collection that are defined as `DataType.BLOB`.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default

        Raises:
            `pydantic.ValidationError` if `image_fields` is not a `list`.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Img2VecNeuralConfigNamed(imageFields=image_fields),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def multi2vec_clip(
        name: str,
        image_fields: Optional[Union[List[str], List[Multi2VecField]]] = None,
        text_fields: Optional[Union[List[str], List[Multi2VecField]]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `multi2vec_clip` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-gpt4all)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Multi2VecClipNamed(
                imageFields=_map_multi2vec_fields(image_fields),
                textFields=_map_multi2vec_fields(text_fields),
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def multi2vec_bind(
        name: str,
        audio_fields: Optional[Union[List[str], List[Multi2VecField]]] = None,
        depth_fields: Optional[Union[List[str], List[Multi2VecField]]] = None,
        image_fields: Optional[Union[List[str], List[Multi2VecField]]] = None,
        imu_fields: Optional[Union[List[str], List[Multi2VecField]]] = None,
        text_fields: Optional[Union[List[str], List[Multi2VecField]]] = None,
        thermal_fields: Optional[Union[List[str], List[Multi2VecField]]] = None,
        video_fields: Optional[Union[List[str], List[Multi2VecField]]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `multi2vec_bind` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-gpt4all)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Multi2VecBindNamed(
                audioFields=_map_multi2vec_fields(audio_fields),
                depthFields=_map_multi2vec_fields(depth_fields),
                imageFields=_map_multi2vec_fields(image_fields),
                IMUFields=_map_multi2vec_fields(imu_fields),
                textFields=_map_multi2vec_fields(text_fields),
                thermalFields=_map_multi2vec_fields(thermal_fields),
                videoFields=_map_multi2vec_fields(video_fields),
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def ref2vec_centroid(
        name: str,
        reference_properties: List[str],
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        method: Literal["mean"] = "mean",
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `ref2vec_centroid` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-gpt4all)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Ref2VecCentroidConfigNamed(
                referenceProperties=reference_properties,
                method=method,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_azure_openai(
        name: str,
        resource_name: str,
        deployment_id: str,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        source_properties: Optional[List[str]] = None,
        vectorize_collection_name: bool = True,
        base_url: Optional[AnyHttpUrl] = None,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec_azure_openai` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-gpt4all)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecAzureOpenAIConfigNamed(
                source_properties=source_properties,
                baseURL=base_url,
                resourceName=resource_name,
                deploymentId=deployment_id,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_gpt4all(
        name: str,
        source_properties: Optional[List[str]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec_gpt4all` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-gpt4all)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecGPT4AllConfigNamed(
                source_properties=source_properties,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_huggingface(
        name: str,
        source_properties: Optional[List[str]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
        model: Optional[str] = None,
        passage_model: Optional[str] = None,
        query_model: Optional[str] = None,
        endpoint_url: Optional[AnyHttpUrl] = None,
        wait_for_model: Optional[bool] = None,
        use_gpu: Optional[bool] = None,
        use_cache: Optional[bool] = None,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec_huggingface` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-huggingface)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
            `model`
                The model to use. Defaults to `None`, which uses the server-defined default.
            `passage_model`
                The passage model to use. Defaults to `None`, which uses the server-defined default.
            `query_model`
                The query model to use. Defaults to `None`, which uses the server-defined default.
            `endpoint_url`
                The endpoint URL to use. Defaults to `None`, which uses the server-defined default.
            `wait_for_model`
                Whether to wait for the model to be loaded. Defaults to `None`, which uses the server-defined default.
            `use_gpu`
                Whether to use the GPU. Defaults to `None`, which uses the server-defined default.
            `use_cache`
                Whether to use the cache. Defaults to `None`, which uses the server-defined default.

        Raises:
            `pydantic.ValidationError` if the arguments passed to the function are invalid.
                It is important to note that some of these variables are mutually exclusive.
                    See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-huggingface) for more details.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecHuggingFaceConfigNamed(
                source_properties=source_properties,
                model=model,
                passageModel=passage_model,
                queryModel=query_model,
                endpointURL=endpoint_url,
                waitForModel=wait_for_model,
                useGPU=use_gpu,
                useCache=use_cache,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_palm(
        name: str,
        project_id: str,
        source_properties: Optional[List[str]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
        api_endpoint: Optional[AnyHttpUrl] = None,
        model_id: Optional[str] = None,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec_palm` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-palm)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `project_id`
                The project ID to use, REQUIRED.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
            `api_endpoint`
                The API endpoint to use. Defaults to `None`, which uses the server-defined default.
            `model_id`
                The model ID to use. Defaults to `None`, which uses the server-defined default.

        Raises:
            `pydantic.ValidationError` if `api_endpoint` is not a valid URL.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecPalmConfigNamed(
                source_properties=source_properties,
                projectId=project_id,
                apiEndpoint=api_endpoint,
                modelId=model_id,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_transformers(
        name: str,
        source_properties: Optional[List[str]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
        pooling_strategy: Literal["masked_mean", "cls"] = "masked_mean",
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec_transformers` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-transformers)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
            `pooling_strategy`
                The pooling strategy to use. Defaults to `masked_mean`.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecTransformersConfigNamed(
                source_properties=source_properties,
                poolingStrategy=pooling_strategy,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )

    @staticmethod
    def text2vec_jinaai(
        name: str,
        source_properties: Optional[List[str]] = None,
        vector_index_config: Optional[_VectorIndexConfigCreate] = None,
        vectorize_collection_name: bool = True,
        model: Optional[Union[JinaModels, str]] = None,
    ) -> _NamedVectorConfigCreate:
        """Create a named vector using the `text2vec-jinaai` model.

        See the [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-jinaai)
        for detailed usage.

        Arguments:
            `name`
                The name of the named vector.
            `source_properties`
                Which properties should be included when vectorizing. By default all text properties are included.
            `vector_index_config`
                The configuration for Weaviate's vector index. Use wvc.config.Configure.VectorIndex to create a vector index configuration. None by default
            `vectorize_collection_name`
                Whether to vectorize the collection name. Defaults to `True`.
            `model`
                The model to use. Defaults to `None`, which uses the server-defined default.
                See the
                [documentation](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-jinaai#available-models) for more details.
        """
        return _NamedVectorConfigCreate(
            name=name,
            vectorizer=_Text2VecJinaConfigNamed(
                source_properties=source_properties,
                model=model,
                vectorizeClassName=vectorize_collection_name,
            ),
            vector_index_config=vector_index_config,
        )
