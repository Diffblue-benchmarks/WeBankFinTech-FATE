package com.webank.ai.fate.serving.federatedml;

import com.webank.ai.fate.core.constant.StatusCode;
import com.webank.ai.fate.core.mlmodel.buffer.PipelineProto;
import com.webank.ai.fate.serving.federatedml.model.BaseModel;
import com.webank.ai.fate.serving.federatedml.DSLParser;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class PipelineTask {
    private List<BaseModel> pipeLineNode = new ArrayList<>();
    private DSLParser dslParser = new DSLParser();
    private String modelPackage = "com.webank.ai.fate.serving.federatedml.model";
    private static final Logger LOGGER = LogManager.getLogger();

    public int initModel(Map<String, byte[]> modelProtoMap) {
        LOGGER.info("start init Pipeline");
        try {
            Map<String, byte[]> newModelProtoMap = changeModelProto(modelProtoMap);
            LOGGER.info("modelProtoMap is {}", modelProtoMap);
            LOGGER.info("newModelProtoMap is {}", newModelProtoMap);
            String pipelineProtoName = "pipeline.Pipeline";
            LOGGER.info("new model proto map is {}", newModelProtoMap.get(pipelineProtoName));
            PipelineProto.Pipeline pipeLineProto = PipelineProto.Pipeline.parseFrom(newModelProtoMap.get(pipelineProtoName));
            LOGGER.info("Finish get Pipeline proto");
            String dsl = pipeLineProto.getInferenceDsl().toStringUtf8(); //inference_dsl;
            dslParser.parseDagFromDSL(dsl);
            ArrayList<String> components = dslParser.getAllComponent();
            HashMap<String, String> componentModuleMap = dslParser.getComponentModuleMap();
            
            for (int i = 0; i < components.size(); ++i) {
            	String componentName = components.get(i);
            	String className = componentModuleMap.get(componentName);
            	LOGGER.info("Start get className:{}", className);
            	try {
                    Class modelClass = Class.forName(this.modelPackage + "." + className);
                    BaseModel mlNode = (BaseModel) modelClass.getConstructor().newInstance();
                    byte[] protoMeta = newModelProtoMap.get(componentName + ".Meta");
                    LOGGER.info("proto meta is {}", protoMeta);
                    byte[] protoParam = newModelProtoMap.get(componentName + ".Param");
                    LOGGER.info("proto param is {}", protoParam);
                    mlNode.initModel(protoMeta, protoParam);

                    pipeLineNode.add(mlNode);
                    LOGGER.info(" Add class {} to pipeline task list", className);
                } catch (Exception ex) {
                    LOGGER.warn("Can not instance {} class", className);
                }
            }
            
        } catch (Exception ex) {
            ex.printStackTrace();
            LOGGER.info("Pipeline init catch error:{}", ex);
        }
        LOGGER.info("Finish init Pipeline");
        return StatusCode.OK;
    }

    public Map<String, Object> predict(Map<String, Object> inputData, Map<String, Object> predictParams) {
        LOGGER.info("Start Pipeline predict use {} model node.", this.pipeLineNode.size());
        List<Map<String, Object>> outputData = new ArrayList<>();
        for (int i = 0; i < this.pipeLineNode.size(); i++) {
            LOGGER.info(this.pipeLineNode.get(i).getClass().getName());
            List<Map<String, Object>> inputs = new ArrayList<>();
            HashSet<Integer> upInputComponents = this.dslParser.getUpInputComponents(i);
            LOGGER.info("upInputComponents is {}", upInputComponents);
            if (upInputComponents != null) {
            	Iterator<Integer> iters = upInputComponents.iterator();
            	while (iters.hasNext()) {
            	    Integer upInput = iters.next();
            	    if (upInput == -1) {
            		inputs.add(inputData);
            	    } else {
            	        inputs.add(outputData.get(upInput));
            	    }
            	}
            } else {
            	inputs.add(inputData);
            }
            LOGGER.info("input data is {}", inputs);
            outputData.add(this.pipeLineNode.get(i).predict(inputs, predictParams));
            
            LOGGER.info("finish mlNone:{}", i);
        }
        LOGGER.info("Finish Pipeline predict");
        LOGGER.info("Finish Pipeline predict, outputData is {}", outputData);
        return outputData.get(outputData.size() - 1);
    }
    
    private HashMap<String, byte[]> changeModelProto(Map<String, byte[]> modelProtoMap) {
    	HashMap<String, byte[]> newModelProtoMap = new HashMap<String, byte[]>();
    	for (Map.Entry<String, byte[]> entry: modelProtoMap.entrySet()) {
    		String key = entry.getKey();
    		if (!key.equals("pipeline.Pipeline")) {
    			String[] componentNameSegments = key.split("\\.", -1);
    			if (componentNameSegments.length != 2) {
    				newModelProtoMap.put(entry.getKey(), entry.getValue());
    				continue;
    			}
    			
    			if (componentNameSegments[1].endsWith("Meta")) {
    				newModelProtoMap.put(componentNameSegments[0] + ".Meta", entry.getValue());
    			} else if (componentNameSegments[1].endsWith("Param")) {
    				newModelProtoMap.put(componentNameSegments[0] + ".Param", entry.getValue());
    			}
    		} else {
    			newModelProtoMap.put(entry.getKey(), entry.getValue());
    		}
    	}
    	
    	return newModelProtoMap;
    }
}
