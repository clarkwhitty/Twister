/*
File: SUT.java ; This file is part of Twister.
Version: 2.004

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

import javax.swing.tree.DefaultMutableTreeNode;

public class SUT{
    private String reserved,name,root,id;
    private String locked = "";
    private DefaultMutableTreeNode epsnode;
    
    public String getEPs(){
        return "";
    }
    
    public SUT(String name,String root){
        this.root = root;
        this.name = name;
        this.reserved = "";
    }
    
    public String getRoot(){
        return this.root;
    }
    
    public String getReserved(){
        return reserved;
    }
    
    public void setReserved(String reserved){
        this.reserved = reserved;
    }
    
    public String getID(){
        return this.id;
    }
    
    public void setID(String id){
        this.id = id;
    }
    
    public String getLock(){
        return this.locked;
    }
    
    public void setLock(String locked){
        this.locked = locked;
    }
    
    public String getName(){
        return name;
    }
    
    public void setName(String name){
        this.name=name;
    }
    
    public DefaultMutableTreeNode getEPNode(){
        return epsnode;
    }
    
    public void setEPNode(DefaultMutableTreeNode epsnode){
        this.epsnode = epsnode;
    }
    
    public String toString(){
        if(!reserved.equals("")){
            return this.name + " - Reserved by: "+this.reserved;
        } else if(!locked.equals("")){
            return this.name + " - Locked by: "+this.locked;
        } else{
            return this.name;
        }
    }
}