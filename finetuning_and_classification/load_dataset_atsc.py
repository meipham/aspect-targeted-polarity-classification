# coding=utf-8
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
"""TODO: Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os
import datasets
import ast


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
authors={huggingface, Inc.
},
year={2020}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to solve this great NLP task and is crafted with a lot of care. 
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = ""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = ""

_ASPECTS = [
    'Bao_bì đóng_gói',
    'Chất_lượng chung',
    'Chức_năng tiêu_hóa',
    'Chức_năng điều_hành',
    'Cân nặng',
    'Dinh_dưỡng',
    'Dị_ứng',
    'Dịch_vụ giao hàng',
    'Dịch_vụ khách_hàng',
    'Giá',
    'Hương_vị',
    'Hướng_dẫn sử_dụng',
    'Hạn sử_dụng',
    'Hấp_thụ',
    'Hệ_miễn_dịch',
    'Hệ_thống thương_mại_điện_tử',
    'Khuyến_mại',
    'Kết_cấu bột',
    'Nguồn_gốc xuất_xứ',
    'Ngủ',
    'Nhãn_hiệu',
    'Nóng',
    'Nội_dung Tiếp_thị điện_tử',
    'Phát_triển thể_chất',
    'Phát_triển trí_não',
    'Phân_phối',
    'Quà tặng',
    'Thành_phần',
    'Thương_mại_điện_tử',
    'Tiếp_thị điện_tử',
    'Tiện_lợi',
    'Tuổi']

class ARDatasetConfig(datasets.BuilderConfig):
    """BuilderConfig for SQUAD."""

    def __init__(self, **kwargs):
        """BuilderConfig for SQUAD.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ARDatasetConfig, self).__init__(**kwargs)


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case

mapper = {
    "-1": "NEG",
    "0": "NEU", 
    "1": "POS"
}
class ARDataset(datasets.GeneratorBasedBuilder):
    
    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
                "label": datasets.ClassLabel(names=["POS","NEU","NEG"])
                #These are the features of your dataset like images, labels ...
            }
        )

        return datasets.DatasetInfo(
            features=features,  # Here we define them above because they are different between the two configurations

        )

    def _split_generators(self, dl_manager):

        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive 
        data_files = dict()

        # Get the train file
        try:
            data_files.update({"train": self.config.data_files['train']})
        except: 
            data_files.update({"train": None})
        

        # Get validate file
        try:
            data_files.update({"validation": self.config.data_files['validation']})
        except: 
            data_files.update({"validation": None})
            
        # Get test file
        try:
            data_files.update({"test": self.config.data_files['test']})
        except: 
            data_files.update({"test": None})
        

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_files["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_files["validation"],
                    "split": "validation"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_files["test"],
                    "split": "test"
                },
            )
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        if filepath is not None:
            with open(filepath, encoding="utf-8") as csv_file:
                
                csv_reader = csv.reader(
                    csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
                )
                next(csv_reader)  # Skip header row.
                for row in csv_reader:
                    id_, sentence1, sentence2, label = row
                    yield id_, {
                        "sentence1": sentence1.strip('"'), 
                        "sentence2": sentence2.strip('"'),
                        "label": mapper[label]
                        }