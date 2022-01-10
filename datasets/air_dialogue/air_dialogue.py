# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""AirDialogue: A large dataset for goal oriented conversations."""


import json

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{wei-etal-2018-airdialogue,
    title = "{A}ir{D}ialogue: An Environment for Goal-Oriented Dialogue Research",
    author = "Wei, Wei  and
      Le, Quoc  and
      Dai, Andrew  and
      Li, Jia",
    booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
    month = oct # "-" # nov,
    year = "2018",
    address = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D18-1419",
    doi = "10.18653/v1/D18-1419",
    pages = "3844--3854",
    abstract = "Recent progress in dialogue generation has inspired a number of studies on dialogue systems that are capable of accomplishing tasks through natural language interactions. A promising direction among these studies is the use of reinforcement learning techniques, such as self-play, for training dialogue agents. However, current datasets are limited in size, and the environment for training agents and evaluating progress is relatively unsophisticated. We present AirDialogue, a large dataset that contains 301,427 goal-oriented conversations. To collect this dataset, we create a context-generator which provides travel and flight restrictions. We then ask human annotators to play the role of a customer or an agent and interact with the goal of successfully booking a trip given the restrictions. Key to our environment is the ease of evaluating the success of the dialogue, which is achieved by using ground-truth states (e.g., the flight being booked) generated by the restrictions. Any dialogue agent that does not generate the correct states is considered to fail. Our experimental results indicate that state-of-the-art dialogue models can only achieve a score of 0.17 while humans can reach a score of 0.91, which suggests significant opportunities for future improvement.",
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
AirDialogue, is a large dataset that contains 402,038 goal-oriented conversations. To collect this dataset, we create a contextgenerator which provides travel and flight restrictions. Then the human annotators are asked to play the role of a customer or an agent and interact with the goal of successfully booking a trip given the restrictions.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://worksheets.codalab.org/worksheets/0xa79833f4b3c24f4188cee7131b120a59"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "cc-by-nc-4.0"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "air_dialogue_data": "https://storage.googleapis.com/airdialogue/airdialogue_data.tar.gz",
    "air_dialogue_kb": "https://storage.googleapis.com/airdialogue/airdialogue_data.tar.gz",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class AirDialogue(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="air_dialogue_data", version=VERSION, description="This part of my dataset covers the dialog files"
        ),
        datasets.BuilderConfig(
            name="air_dialogue_kb", version=VERSION, description="This part of my dataset covers the knowledge base"
        ),
    ]

    DEFAULT_CONFIG_NAME = (
        "air_dialogue_data"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if (
            self.config.name == "air_dialogue_data"
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "action": {
                        "status": datasets.Value("string"),
                        "name": datasets.Value("string"),
                        "flight": datasets.features.Sequence(datasets.Value("int32")),
                    },
                    "intent": {
                        "return_month": datasets.Value("string"),
                        "return_day": datasets.Value("string"),
                        "max_price": datasets.Value("int32"),
                        "departure_airport": datasets.Value("string"),
                        "max_connections": datasets.Value("int32"),
                        "departure_day": datasets.Value("string"),
                        "goal": datasets.Value("string"),
                        "departure_month": datasets.Value("string"),
                        "name": datasets.Value("string"),
                        "return_airport": datasets.Value("string"),
                    },
                    "timestamps": datasets.features.Sequence(datasets.Value("int64")),
                    "dialogue": datasets.features.Sequence(datasets.Value("string")),
                    "expected_action": {
                        "status": datasets.Value("string"),
                        "name": datasets.Value("string"),
                        "flight": datasets.features.Sequence(datasets.Value("int32")),
                    },
                    "search_info": [
                        {
                            "button_name": datasets.Value("string"),
                            "field_name": datasets.Value("string"),
                            "field_value": datasets.Value("string"),
                            "timestmamp": datasets.Value("int64"),
                        },
                    ],
                    "correct_sample": datasets.Value("bool_"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "kb": [
                        {
                            "airline": datasets.Value("string"),
                            "class": datasets.Value("string"),
                            "departure_airport": datasets.Value("string"),
                            "departure_day": datasets.Value("string"),
                            "departure_month": datasets.Value("string"),
                            "departure_time_num": datasets.Value("int32"),
                            "flight_number": datasets.Value("int32"),
                            "num_connections": datasets.Value("int32"),
                            "price": datasets.Value("int32"),
                            "return_airport": datasets.Value("string"),
                            "return_day": datasets.Value("string"),
                            "return_month": datasets.Value("string"),
                            "return_time_num": datasets.Value("int32"),
                        },
                    ],
                    "reservation": datasets.Value("int32"),
                }
            )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URLs[self.config.name]
        archive = dl_manager.download(my_urls)
        if self.config.name == "air_dialogue_data":
            train = "airdialogue_data/airdialogue/train_data.json"
            dev = "airdialogue_data/airdialogue/dev_data.json"
        else:
            train = "airdialogue_data/airdialogue/train_kb.json"
            dev = "airdialogue_data/airdialogue/dev_kb.json"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": train,
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": dev,
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, files):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        for path, f in files:
            if path == filepath:
                for id_, row in enumerate(f):
                    row = row.decode("utf-8")
                    data = json.loads(row)
                    if self.config.name == "air_dialogue_data":

                        intent = {
                            "return_month": data["intent"]["return_month"],
                            "return_day": data["intent"]["return_day"],
                            "max_price": data["intent"]["max_price"],
                            "departure_airport": data["intent"]["departure_airport"],
                            "max_connections": data["intent"].get("max_connections", -1),
                            "departure_day": data["intent"]["departure_day"],
                            "goal": data["intent"]["goal"],
                            "departure_month": data["intent"]["departure_month"],
                            "name": data["intent"]["name"],
                            "return_airport": data["intent"]["return_airport"],
                        }

                        search_info = (
                            []
                            if "search_info" not in data
                            else [
                                {
                                    "button_name": search_info.get("button_name", ""),
                                    "field_name": search_info.get("field_name", ""),
                                    "field_value": search_info.get("field_value", ""),
                                    "timestmamp": search_info["timestmamp"],
                                }
                                for search_info in data["search_info"]
                            ]
                        )

                        yield id_, {
                            "action": {key: data["action"][key] for key in data["action"]},
                            "intent": intent,
                            "timestamps": data["timestamps"],
                            "dialogue": data["dialogue"],
                            "expected_action": {key: data["expected_action"][key] for key in data["expected_action"]},
                            "search_info": search_info,
                            "correct_sample": data["correct_sample"],
                        }

                    else:

                        kb = [
                            {
                                "airline": kb["airline"],
                                "class": kb["class"],
                                "departure_airport": kb["departure_airport"],
                                "departure_day": kb["departure_day"],
                                "departure_month": kb["departure_month"],
                                "departure_time_num": kb["departure_time_num"],
                                "flight_number": kb["flight_number"],
                                "num_connections": kb["num_connections"],
                                "price": kb["price"],
                                "return_airport": kb["return_airport"],
                                "return_day": kb["return_day"],
                                "return_month": kb["return_month"],
                                "return_time_num": kb["return_time_num"],
                            }
                            for kb in data["kb"]
                        ]

                        yield id_, {
                            "kb": kb,
                            "reservation": data["reservation"],
                        }
                break
