import os
import yaml
import json
import re
from typing import List
from yaml.reader import Reader


"""
Format
"Filename": [[Main Key (for identification)], [Item containing string]]
"""
primary_key_rules = {
    "Achievement": [["id"], ["name", "description"]],
    # "AchievementProgress": [[], []],
    # "AppReview": [[], []],
    # "AssetDownload": [[], []],
    # "Bgm": [[], []],
    "Character": [["id"], ["lastName", "firstName", "alphabetLastName", "alphabetFirstName"]],
    "CharacterAdv": [["characterId"], ["name", "regexp"]],
    # "CharacterColor": [[], []],
    "CharacterDearnessLevel": [["characterId", "dearnessLevel"], ["produceConditionDescription"]],
    # "CharacterDearnessStoryGashaCampaign": [[], []],
    "CharacterDetail": [["characterId", "type", "order"], ["content"]],
    # "CharacterProduceStory": [[], []],
    "CharacterPushMessage": [["characterId", "type", "number"], ["title", "message"]],
    # "CharacterTrueEndAchievement": [[], []],
    # "CharacterTrueEndBonus": [[], []],
    "CoinGashaButton": [["id"], ["name", "description"]],
    "ConditionSet": [["id", "number"], ["description"]],
    # "ConsumptionSet": [[], []],
    "Costume": [["id"], ["name", "description"]],
    # "CostumeColorGroup": [[], []],
    # "CostumeGroup": [[], []],
    "CostumeHead": [["id"], ["name", "description"]],
    # "CostumeMotion": [[], []],
    # "CostumePhotoGroup": [[], []],
    # "DearnessBackground": [[], []],
    # "DearnessBgm": [[], []],
    # "DearnessBoostBgm": [[], []],
    # "DearnessMotion": [[], []],
    # "DearnessStoryCampaign": [[], []],
    # "DeepLinkTransition": [[], []],
    "EffectGroup": [["id"], ["name"]],
    "EventLabel": [["eventType"], ["name"]],
    # "EventStoryCampaign": [[], []],
    # "ExamInitialDeck": [[], []],
    # "ExamMotion": [[], []],
    # "ExamOutGameMotion": [[], []],
    # "ExamSetting": [[], []],
    # "ExamSimulation": [[], []],
    "ExchangeItemCategory": [["exchangeId", "number", "categoryType", "resourceType", "itemType"], ["name"]],
    "FeatureLock": [["tutorialType"], ["name", "description", "routeDescription"]],
    # "ForceAppVersion": [[], []],
    # "GashaAnimation": [[], []],
    # "GashaAnimationStep": [[], []],
    "GashaButton": [["id", "order"], ["name", "description"]],
    # "GuildDonationItem": [[], []],
    # "GuildReaction": [[], []],
    "GvgRaid": [["id", "order"], ["name"]],
    # "GvgRaidStageLoop": [[], []],
    "HelpCategory": [["id", "order"], ["name", "texts", "hiddenHelpList"]],
    "HelpContent": [["helpCategoryId", "id", "order"], ["name", "detailUrl"]],
    # "HelpInfo": [["type", "openHelpCategoryId", "openHelpContentId"], ["helpCategoryIds"]],
    # "HomeBoard": [[], []],
    # "HomeMonitor": [[], []],
    # "HomeMotion": [[], []],
    # "HomeTime": [[], []],
    "IdolCard": [["id"], ["name"]],
    # "IdolCardLevelLimit": [[], []],
    # "IdolCardLevelLimitProduceSkill": [[], []],
    # "IdolCardLevelLimitStatusUp": [[], []],
    # "IdolCardPiece": [[], []],
    # "IdolCardPieceQuantity": [[], []],
    # "IdolCardPotential": [[], []],
    # "IdolCardPotentialProduceSkill": [[], []],
    # "IdolCardSimulation": [[], []],
    # "IdolCardSkin": [[], []],
    # "IdolCardSkinSelectReward": [[], []],
    # "IdolCardSkinUnit": [[], []],
    # "InvitationMission": [[], []],
    # "InvitationPointReward": [[], []],
    "Item": [["id"], ["name", "description", "acquisitionRouteDescription"]],
    # "JewelConsumptionCount": [[], []],
    # "LimitItem": [[], []],
    "Localization": [["id"], ["description"]],
    # "LoginBonusMotion": [[], []],
    "MainStoryChapter": [["mainStoryPartId", "id"], ["title", "description"]],
    "MainStoryPart": [["id"], ["title"]],
    "MainTask": [["mainTaskGroupId", "number"], ["title", "description", "homeDescription"]],
    "MainTaskGroup": [["id"], ["title"]],
    # "MainTaskIcon": [[], []],
    "Media": [["id"], ["name"]],
    "MeishiBaseAsset": [["id"], ["name"]],
    # "MeishiBaseColor": [[], []],
    "MeishiIllustrationAsset": [["id"], ["name"]],
    # "MeishiTextColor": [[], []],
    # "MemoryAbility": [[], []],
    # "MemoryExchangeItem": [[], []],
    # "MemoryExchangeItemQuantity": [[], []],
    "MemoryGift": [["id"], ["name"]],
    "MemoryTag": [["id"], ["defaultName"]],
    "Mission": [["id"], ["name"]],
    # "MissionDailyRelease": [[], []],
    # "MissionDailyReleaseGroup": [[], []],
    "MissionGroup": [["id"], ["name"]],
    "MissionPanelSheet": [["missionPanelSheetGroupId", "number"], ["name"]],
    "MissionPanelSheetGroup": [["id"], ["name"]],
    "MissionPass": [["id"], ["name", "description"]],
    "MissionPassPoint": [["id"], ["name"]],
    # "MissionPassProgress": [[], []],
    "MissionPoint": [["id"], ["name"]],
    # "MissionPointRewardSet": [[], []],
    # "MissionProgress": [[], []],
    # "Money": [[], []],
    "Music": [["id"], ["title", "displayTitle", "lyrics", "composer", "arranger"]],
    # "MusicHot": [[], []],
    # "MusicSinger": [[], []],
    "PhotoBackground": [["id"], ["name"]],
    # "PhotoFacialLookTarget": [[], []],
    "PhotoFacialMotionGroup": [["id", "number"], ["name"]],
    # "PhotoLookTargetVoiceCharacter": [[], []],
    "PhotoPose": [["id"], ["name"]],
    # "PhotoReactionVoiceGroup": [[], []],
    # "PhotoWaitVoiceCharacter": [[], []],
    # "PhotoWaitVoiceGroup": [[], []],
    "Produce": [["id"], ["name"]],
    "ProduceAdv": [["produceType", "type"], ["title"]],
    "ProduceCard": [["id", "upgradeCount", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                     "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId",
                     ],
                    ["name", "produceDescriptions.text"]],  # 嵌套
    "ProduceCardCustomize": [["id", "customizeCount", "overwriteProduceCardGrowEffectType"], ["description"]],
    # "ProduceCardCustomizeRarityEvaluation": [[], []],
    # "ProduceCardGrowEffect": [[], []],
    # "ProduceCardPool": [[], []],
    # "ProduceCardRandomPool": [[], []],
    "ProduceCardSearch": [["id", 
                           "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                           "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                          ["produceDescriptions.text"]],  # 嵌套
    # "ProduceCardSimulation": [[], []],
    # "ProduceCardSimulationGroup": [[], []],
    # "ProduceCardStatusEffect": [[], []],
    "ProduceCardStatusEnchant": [["id", "produceExamTriggerId", "triggerCount", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                  "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                                 ["produceDescriptions.text"]],  # 嵌套
    "ProduceCardTag": [["id"], ["name"]],
    # "ProduceChallengeCharacter": [[], []],
    "ProduceChallengeSlot": [["id", "produceId", "number"], ["unlockDescription"]],
    # "ProduceCharacter": [[], []],
    "ProduceCharacterAdv": [["assetId"], ["title"]],
    "ProduceDescription": [["id"], ["name", "swapName"]],
    "ProduceDescriptionExamEffect": [["type"], ["name"]],
    "ProduceDescriptionLabel": [["id", 
                                 "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                 "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"], 
                                ["name", "produceDescriptions.text"]],
    "ProduceDescriptionProduceCardGrowEffect": [["type"], ["name"]],
    "ProduceDescriptionProduceCardGrowEffectType": [["type"], ["name", "produceCardCustomizeTemplate"]],
    # "ProduceDescriptionProduceCardMovePosition": [[], []],
    "ProduceDescriptionProduceEffect": [["type"], ["name"]],
    "ProduceDescriptionProduceEffectType": [["type"], ["name"]],
    "ProduceDescriptionProduceExamEffectType": [["type"], ["name", "swapName"]],
    "ProduceDescriptionProducePlan": [["type"], ["name"]],
    "ProduceDescriptionProducePlanType": [["type"], ["name"]],
    "ProduceDescriptionProduceStep": [["type"], ["name"]],
    "ProduceDescriptionSwap": [["id", "swapType"], ["text"]],
    "ProduceDrink": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                      "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                     ["name", "produceDescriptions.text"]],  # 嵌套
    # "ProduceDrinkEffect": [[], []],
    # "ProduceEffect": [[], []],
    # "ProduceEffectIcon": [[], []],
    "ProduceEventCharacterGrowth": [["characterId", "number"], ["title", "description"]],
    # "ProduceEventSupportCard": [[], []],
    # "ProduceExamAutoCardSelectEvaluation": [[], []],
    # "ProduceExamAutoEvaluation": [[], []],
    # "ProduceExamAutoGrowEffectEvaluation": [[], []],
    # "ProduceExamAutoPlayCardEvaluation": [[], []],
    # "ProduceExamAutoResourceEvaluation": [[], []],
    # "ProduceExamAutoTriggerEvaluation": [[], []],
    # "ProduceExamBattleConfig": [[], []],
    # "ProduceExamBattleNpcGroup": [[], []],
    "ProduceExamBattleNpcMob": [["id"], ["name"]],
    # "ProduceExamBattleScoreConfig": [[], []],
    "ProduceExamEffect": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                          "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                          ["produceDescriptions.text"]],  # 嵌套List Obj
    "ProduceExamGimmickEffectGroup": [["id", "priority", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                      "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                                      ["produceDescriptions.text"]],  # 嵌套List Obj
    "ProduceExamStatusEnchant": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                  "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                                 ["produceDescriptions.text"]],  # 嵌套List Obj
    "ProduceExamTrigger": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                            "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId",
                            ],
                           ["produceDescriptions.text"]],  # 嵌套List Obj
    # "ProduceGrade": [[], []],
    "ProduceGroup": [["id"], ["name", "description"]],
    # "ProduceGuide": [[], []],
    "ProduceGuideProduceCardCategory": [["id"], ["label"]],
    "ProduceGuideProduceCardCategoryGroup": [["id"], ["description"]],
    "ProduceGuideProduceCardSampleDeckCategory": [["id"], ["label"]],
    # "ProduceGuideProduceCardSampleDeckCategoryGroup": [[], []],
    # "ProduceGroupLiveCommon": [[], []],
    "ProduceHighScore": [["id"], ["name"]],
    "ProduceItem": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                     "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                    ["name", "produceDescriptions.text"]],  # 嵌套List Obj
    # "ProduceItemChallengeGroup": [[], []],
    # "ProduceItemEffect": [[], []],
    # "ProduceItemSimulation": [[], []],
    # "ProduceItemSimulationGroup": [[], []],
    # "ProduceLive": [["musicId", "type"], ["forceUnlockConditionSetId", "unlockConditionSetId", "thumbnailAssetId" ,"environmentAssetId", "timelineAssetId", "beforeAdvAssetId", "afterAdvAssetId", "liveMusicAssetId", "motionAssetIds", "unitLiveThumbnailAssetCharacterIds", "unitLiveThumbnailAssetIds", "liveOverrideAssetId", "additionalActorAssetIds"]],
    # "ProduceLiveCommon": [[], []],
    "ProduceNavigation": [["id", "number"], ["description"]],
    # "ProduceNextIdolAuditionMasterRankingSeason": [[], []],
    # "ProduceResultMotion": [[], []],
    # "ProducerLevel": [[], []],
    # "ProduceScheduleBackground": [[], []],
    # "ProduceScheduleMotion": [[], []],
    # "ProduceSetting": [[], []],
    "ProduceSkill": [["id", "level", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                      "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                     ["produceDescriptions.text"]],  # 嵌套List Obj
    # "ProduceStartMotion": [[], []],
    # "ProduceStepAuditionCharacter": [[], []],
    # "ProduceStepAuditionDifficulty": [[], []],
    # "ProduceStepAuditionMotion": [[], []],
    "ProduceStepEventDetail": [["id", 
                                "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType",
                                "produceDescriptions.examEffectType",
                                "produceDescriptions.produceCardCategory",
                                "produceDescriptions.produceCardMovePositionType",
                                "produceDescriptions.produceStepType", "produceDescriptions.targetId"
                                ],
                               ["produceDescriptions.text"]],  # 嵌套List Obj
    "ProduceStepEventSuggestion": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                    "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId",
                                    ],
                                   ["produceDescriptions.text"]],  # 嵌套List Obj
    # "ProduceStepFanPresentMotion": [[], []],
    "ProduceStepLesson": [["id"], ["name"]],
    # "ProduceStepLessonLevel": [[], []],
    # "ProduceStepSelfLesson": [[], []],
    # "ProduceStepSelfLessonMotion": [[], []],
    # "ProduceStepTransition": [[], []],
    "ProduceStory": [["id"], ["title", "produceEventHintProduceConditionDescriptions"]],
    # "ProduceStoryGroup": [[], []],
    # "ProduceTrigger": [[], []],
    # "ProduceWeekMotion": [[], []],
    # "PvpRateCommonProduceCard": [[], []],
    "PvpRateConfig": [["id"], ["description"]],
    # "PvpRateMotion": [[], []],
    # "PvpRateUnitSlotUnlock": [[], []],
    # "ResultGradePattern": [[], []],
    "Rule": [["type", "platformType", "number"], ["html"]],
    "SeminarExamTransition": [["examEffectType", "isLessonInt", "seminarExamId"], ["description", "seminarExamGroupName", "seminarExamName"]],
    "Setting": [["id"], ["initialUserName", "banWarningMessage"]],
    "Shop": [["id"], ["name"]],
    "ShopItem": [["id"], ["name"]],
    # "ShopProduct": [[], []],
    "Story": [["id"], ["title"]],
    "StoryEvent": [["id"], ["title"]],
    "StoryGroup": [["id"], ["title"]],
    "SupportCard": [["id", "upgradeProduceCardProduceDescriptions.produceDescriptionType", "upgradeProduceCardProduceDescriptions.examDescriptionType", "upgradeProduceCardProduceDescriptions.examEffectType", 
                     "upgradeProduceCardProduceDescriptions.produceCardGrowEffectType", "upgradeProduceCardProduceDescriptions.produceCardCategory", "upgradeProduceCardProduceDescriptions.produceCardMovePositionType", "upgradeProduceCardProduceDescriptions.produceStepType"],
                    ["name", "upgradeProduceCardProduceDescriptions.text"]],  # 嵌套List Obj
    # "SupportCardBonus": [[], []],
    "SupportCardFlavor": [["supportCardId", "number"], ["text"]],
    # "SupportCardLevel": [[], []],
    # "SupportCardLevelLimit": [[], []],
    "SupportCardProduceSkillFilter": [["id", "order"], ["title"]],
    # "SupportCardProduceSkillLevelAssist": [[], []],
    # "SupportCardProduceSkillLevelDance": [[], []],
    # "SupportCardProduceSkillLevelVisual": [[], []],
    # "SupportCardProduceSkillLevelVocal": [[], []],
    # "SupportCardSimulation": [[], []],
    # "SupportCardSimulationGroup": [[], []],
    "Terms": [["type"], ["name"]],
    "Tips": [["id"], ["title", "description"]],
    # "TitleAsset": [[], []],
    # "TitleVoice": [[], []],
    "Tower": [["id"], ["title"]],
    # "TowerLayer": [[], []],
    # "TowerLayerExam": [[], []],
    # "TowerLayerRank": [[], []],
    # "TowerTotalClearRankReward": [[], []],
    "Tutorial": [["tutorialType", "idolCardId", "step", "subStep", "navigationType", "navigationPositionType", "tutorialProduceCommandType"], ["texts", "title"]],
    # "TutorialCharacterVoice": [[], []],
    # "TutorialProduce": [[], []],
    "TutorialProduceStep": [["tutorialType", "stepNumber", "tutorialStep", "stepType"], ["name"]],
    # "Voice": [[], []],
    "VoiceGroup": [["id", "voiceAssetId"], ["title"]],
    "VoiceRoster": [["characterId", "assetId"], ["title"]],
    "Work": [["type"], ["name"]],
    # "WorkLevel": [[], []],
    # "WorkLevelReward": [[], []],
    # "WorkMotion": [[], []],
    # "WorkSkip": [[], []],
    # "WorkTime": [[], []],
    # "CostumeWaitMotion": [[], []],
    "Tour": [["id", "storyGroupId", "tourStageTimelineId"], ["name", "liveTicketName"]],
    # "TourStageTimeline": [[], []],
    # "TowerReset": [[], []]
}

TestMode = False

class CustomLoader(yaml.SafeLoader):
    def __init__(self, stream):
        # Override initialization to support specific control characters
        super().__init__(stream)

    def check_printable(self, data):
        """
        Rewrite the check function to allow for non-printable characters (like #x000b)
        """
        for char in data:
            if char == "\x0b":  # Allow vertical tabs
                continue
            if not super().check_printable(char):
                return False
        return True


def save_json(data: list, name: str):
    """
    Main process:
    1. Take the primary key list (primary_keys) and non-primary key list (other_keys) from primary_key_rules[name].
    2. Keep only these fields (split '.' to handle nested/arrays).
    3. If TestMode = True, append "TEST" to the string or string array in the "non-primary key list".
    """
    if not data:
        return None

    # Get the rule corresponding to the name
    rule = primary_key_rules.get(name)
    if not rule or len(rule) < 2:
        return None

    primary_keys = rule[0]  # First column (primary key)
    other_keys = rule[1]    # Second list (TEST may be added)

    # Merge all fields to be retained (first item + second item)
    all_keys = primary_keys + other_keys

    processed_data = []
    for record in data:
        # Construct a new object for the current record, containing only the required fields
        filtered_record = filter_record_fields(
            record,
            all_keys,
            primary_keys,
            other_keys
        )
        processed_data.append(filtered_record)

    # Make sure the first data has all keys
    # This can be removed when the app can parse all keys(also key type) properly.
    # Currently, there is a bug on finding type and local keys from data
    # We must make sure the first data has all keys
    if not sort_records_fields(processed_data, all_keys):
        print(f"Failed to find super key object from {name}")
        
    # Generate the final JSON structure
    
    result = {
        "rules": {
            "primaryKeys": primary_keys
        },
        "data": processed_data
    }

    # Write JSON files
    os.makedirs('./gakumasu-diff/json', exist_ok=True)
    with open(f'gakumasu-diff/json/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return f'gakumasu-diff/json/{name}.json'

def sort_records_fields(records: List[dict], field_paths: list):
    def hasPaths(record:dict, path:list):
        if not path:
            return False
        key = path[0]
        if not isinstance(record, dict) or key not in record:
            return False
        record_value = record[key]
        # No more sub object, we find all objects from record by path
        if len(path) == 1:
            return True
        
        # If there is obj use traversal to find value
        if isinstance(record_value, dict):
            return hasPaths(record_value, path[1:])

        # When obj is list, check all elements
        if isinstance(record_value, list):
            for item in record_value:
                if isinstance(item, dict):
                    if hasPaths(item, path[1:]):
                        # it has all subkeys
                        return True
        # Failed to find value by key
        return False
    for idx in range(len(records)):
        hasAllField = True
        for paths in field_paths:
            path = paths.split(".") 
            if not hasPaths(records[idx], path):
                hasAllField = False
                break
        if hasAllField:
            records.insert(0, records.pop(idx))
            return True
    return False

def filter_record_fields(record: dict, field_paths: list,
                         primary_keys: list, other_keys: list) -> dict:
    """
    Given an original record and a list of field paths field_paths to keep,
    return a new dictionary containing only those fields (and their nested structure).
    If the path is in other_keys and TestMode = True, add "TEST" to the string or list of strings.
    """
    new_record = {}
    for path_str in field_paths:
        path = path_str.split(".")  # "descriptions.type" -> ["descriptions", "type"]
        value = get_nested_value(record, path)
        if value is not None:
            # Append “TEST” to a string / string list value if it belongs to a non-primary key list & TestMode = True
            if TestMode and (path_str in other_keys):
                value = transform_value_for_test_mode(value)
            # Merge the fetched value into new_record, keeping the same nested structure
            merge_nested_value(new_record, path, value)
    return new_record


def get_nested_value(obj, path: list):
    """
    Go deep into obj according to path and get the corresponding value.
    If any step in the middle does not exist, return None.
    If a list is encountered, do the same process for each object in the list and return a list of the same length.
    """
    if not path:
        return obj

    key = path[0]
    if not isinstance(obj, dict) or key not in obj:
        return None

    sub_obj = obj[key]
    # If only the last layer of path is left, return directly
    if len(path) == 1:
        return sub_obj

    # If it is a dictionary, continue to go deeper
    if isinstance(sub_obj, dict):
        return get_nested_value(sub_obj, path[1:])

    # If it is a list, do the same process for each element and return a list
    if isinstance(sub_obj, list):
        results = []
        for item in sub_obj:
            if isinstance(item, dict):
                val = get_nested_value(item, path[1:])
                results.append(val)
            else:
                # If the list is not a dict, you can't go any deeper and can only return None
                results.append(None)
        return results

    # Other cases (numbers, strings, etc.) cannot be further explored
    return None


def merge_nested_value(target_dict: dict, path: list, value):
    """
    Merge value into target_dict according to the hierarchical structure of path.
    If a level is a list, you need to construct a list of the same length in target_dict and then merge them item by item.
    """
    if not path:
        return

    key = path[0]

    # If only the last level of the key is left, write it directly
    if len(path) == 1:
        target_dict[key] = value
        return

    # If value is a list, it means the current layer is a list and needs special processing
    if isinstance(value, list):
        # If target_dict[key] does not exist or is not a list, initialize it to an empty list first
        if key not in target_dict or not isinstance(target_dict[key], list):
            target_dict[key] = [None] * len(value)

        # Traverse each item in value and merge recursively
        for i, v in enumerate(value):
            if v is None:
                continue  # Skip None
            # If target_dict[key][i] has not been created yet, initialize it to dict
            if target_dict[key][i] is None:
                target_dict[key][i] = {}
            # Continue deep merging
            merge_nested_value(target_dict[key][i], path[1:], v)
        return

    # Otherwise, if target_dict[key] does not exist or is not a dictionary, it is initialized to a dictionary
    if key not in target_dict or not isinstance(target_dict[key], dict):
        target_dict[key] = {}

    # Recursively process the remaining paths
    merge_nested_value(target_dict[key], path[1:], value)


def transform_value_for_test_mode(value):
    """
    If it is a string, append "TEST".
    If it is a list of strings, append "TEST" to each item in the list.
    Other types remain unchanged.
    """
    if isinstance(value, str):
        return value + "TEST"
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return [v + "TEST" for v in value]
    return value


# process_list = ["ProduceStepLesson", "SupportCardFlavor"]
process_list = None

def convert_yaml_types(folder_path="./gakumasu-diff/orig"):
    """
    Iterates over all YAML files in a specified folder, loads their contents, and prints the type of each file.
    Automatically replaces tabs in YAML files with spaces.
    """
    if not os.path.isdir(folder_path):
        print(f"The path '{folder_path}' is not a valid folder.")
        return

    for root, _, files in os.walk(folder_path):
        total = len(files)
        for n, file in enumerate(files):
            if file.endswith('.yaml'):
                if process_list:
                    if file[:-5] not in process_list:
                        continue

                file_path = os.path.join(root, file)
                # print(f"\"{file[:-5]}\": [[], []],")
                # continue

                print("Parsing", file_path, f"to json. ({n}/{total})")
                try:
                    # Preprocess file: replace tabs with 4 spaces
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    content = re.sub(r': (\t.*)', r': "\1"', content)  # Replace tab characters
                    content = content.replace("|\n", "|+\n") # Fix literal strings newline chomping

                    # Parsing YAML content
                    # data = yaml.safe_load(content)
                    data = yaml.load(content, CustomLoader)
                    save_json(data, file[:-5])

                    # print(f"文件: {file_path}")
                    # print(f"类型: {type(data)}\n")
                except Exception as e:
                    print(f"Error occured while loading file {file_path}: {e}")


if __name__ == '__main__':
    convert_yaml_types()
