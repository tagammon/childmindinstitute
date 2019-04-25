# -*- coding: utf-8 -*-

###############################################################################
#  Copyright 2013 Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

_modelClasses = {}
_coreModelsRegistered = False


def _registerCoreModels():
    global _coreModelsRegistered
    if _coreModelsRegistered:
        return

    from girder.models import (
        api_key, assetstore, collection, file, folder, group, item, notification, password,
        setting, token, upload, user)

    ModelImporter.registerModel('api_key', api_key.ApiKey)
    ModelImporter.registerModel('assetstore', assetstore.Assetstore)
    ModelImporter.registerModel('collection', collection.Collection)
    ModelImporter.registerModel('file', file.File)
    ModelImporter.registerModel('folder', folder.Folder)
    ModelImporter.registerModel('group', group.Group)
    ModelImporter.registerModel('item', item.Item)
    ModelImporter.registerModel('notification', notification.Notification)
    ModelImporter.registerModel('password', password.Password)
    ModelImporter.registerModel('setting', setting.Setting)
    ModelImporter.registerModel('token', token.Token)
    ModelImporter.registerModel('upload', upload.Upload)
    ModelImporter.registerModel('user', user.User)

    _coreModelsRegistered = True


class ModelImporter(object):
    """
    Any class that wants to have convenient model importing semantics
    should extend/mixin this class.
    """
    @staticmethod
    def model(model, plugin='_core'):
        """
        Call this to get the instance of the specified model. It will be
        lazy-instantiated.

        :param model: The name of the model to get. This must have been
            registered using the :py:meth:`registerModel` method.
        :type model: string
        :param plugin: Plugin identifier (if this is a plugin model).
        :type plugin: str
        :returns: The instantiated model, which is a singleton.
        """
        if not _coreModelsRegistered and plugin == '_core':
            _registerCoreModels()

        if not _modelClasses.get(plugin, {}).get(model):
            raise Exception('Model "%s.%s" is not registered.' % (plugin, model))

        return _modelClasses[plugin][model]()

    @staticmethod
    def registerModel(model, cls, plugin='_core'):
        """
        Use this method to register a model class to a name. Using this, it can
        be referenced via the ``model`` method of this class.

        :param model: The model name.
        :type model: str
        :param plugin: Plugin identifier (if this is a plugin model).
        :type plugin: str
        :param cls: The model class, should be a subclass of
            :py:class:`girder.models.model_base.Model`.
        :type cls: type
        """
        if plugin not in _modelClasses:
            _modelClasses[plugin] = {}
        _modelClasses[plugin][model] = cls

    @staticmethod
    def unregisterModel(model, plugin='_core'):
        del _modelClasses[plugin][model]
